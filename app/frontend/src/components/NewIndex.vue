<template>
  <body>
    <div v-if="isInputComplete" class="split left" id="Input" v-on:keyup.enter="inputParams">
        <h2>Connect to your database</h2>
        <!-- array of strings or numbers -->
        <select required v-model="selected">
          <option disabled="disabled" value="placeholder">Please select database type</option>
          <option v-for="(option, index) in db_options" :value="option" :key="index">{{ option }}</option>   
        </select>
        <br />
        <input
        name="dbHost"
        ref="dbHost"
        value="Type in your host address for connecting"
        />
        <br />
        <input
        name="dbPort"
        ref="dbPort"
        value="Type in your port for connecting, i.e. 3306"
        />
        <br />
        <input
        name="dbName"
        ref="dbName"
        value="Type in the name of your database"
        />
        <br />
        <input
        name="dbUser"
        ref="dbUser"
        value="Type in the username required for connecting"
        />
        <br />
        <h4>Type in your password in the field below</h4>
        <input
        name="dbPassword"
        ref="dbPassword"
        value="Type in the password as well"
        type="password"
        />
        <br />
        <br />
        <h4>Select scan option for finding references in your database</h4>
        <span
        class="options"
        v-for="(option, index) in scan_options"
        :key="index"
        >
        <input
            :id="option"
            :value="option"
            name="table"
            type="radio"
            class="checkbox_option"
            v-model="selected_option"
            v-on:click="checkOne()"
        />
        {{ option }}
        </span>
        <br />
        <br />
        <button class="special_button" v-on:click.prevent="inputParams">
        Run scan of my database!
        </button>
    </div>
    <div v-if="isScanResponse" class="split right" id="Response">
        <h2>Pick your tables to model</h2>
        <br />
        <div class="checkboxes">
        <li v-for="(table, index) in rows['result']" :key="index">
            <input
            :id="table"
            :value="table"
            name="table"
            type="checkbox"
            class="checkbox"
            v-model="selected_pipes"
            />
            {{ table.name }}
        </li>
        </div>
        <br />
        <li class="list_select_all">
        <input
            type="radio"
            class="checkbox_select_all"
            v-on:click="selectAll"
        />
        {{ this.select_all_string }}
        </li>
        <br />
        <button class="special_button" v-on:click="createDataFlow">Create dataflow</button>
    </div>
    <div v-if="isBufferActive" name="buffer" class="split right">
        <span v-html="bufferIcon()"></span>
    </div>
    <div v-if="is404" class="center">
        <span> {{rows}} </span>
    </div>
    <div v-if="isGlobalBufferActive" class="center" id="Buffer">
      <span v-html="bufferIcon()"></span>
    </div>
    <div v-if="isSesamResponse" class="sesam" id="sesamResponse">
      <br />
      <br />
      <h2>{{ result["sesam_result"] }}</h2>
    </div>
  </body>
</template>
  
<script>
import api from "../api";
export default {
  name: "NewIndex",
  data: () => {
    return {
      isCheckAll: false,
      isSesamResponse: false,
      isScanResponse: false,
      isBufferActive: false,
      isGlobalBufferActive: false,
      isSesamInt: false,
      select_all_string: "Select All",
      isInputComplete: true,
      is404: false,
      rows: "{{tables}}",
      selected: "placeholder",
      db_options: ['MySQL', 'PostgreSQL', 'MsSQL'],
      scan_options: [
        "No references",
        "Foreign Key references",
        "Index references",
      ],
      selected_option: [],
      selected_pipes: []
    };
  },
  methods: {
    async inputParams() {
      let dbase = this.selected;
      let dbHost = this.$refs.dbHost.value;
      let dbPort = this.$refs.dbPort.value;
      let dbName = this.$refs.dbName.value;
      let dbUser = this.$refs.dbUser.value;
      let dbPassword = this.$refs.dbPassword.value;
      let option = this.selected_option;
      // eslint-disable-next-line no-console
      //console.log(option)
      this.isBufferActive = true;
      this.isSesamInt = true;
      // http://localhost/backend_autoconnect/ http://localhost:5000/ # For running locally.
      await fetch("http://localhost/backend_autoconnect/connectors", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          dbase: dbase,
          dbHost: dbHost,
          dbPort: dbPort,
          dbName: dbName,
          dbUser: dbUser,
          dbPassword: dbPassword,
          option: option,
        }),
      });
      this.selected = "placeholder";
      this.$refs.dbHost.value = "Type in your host address for connecting";
      this.$refs.dbPort.value = "Type in your port for connecting, i.e. 3306";
      this.$refs.dbName.value = "Type in the name of your database";
      this.$refs.dbUser.value = "Type in the username required for connecting";
      this.$refs.dbPassword.value = [];
      this.scanResponse();
    },
    bufferIcon() {
      return '<img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" alt="Loading GIF">';
    },
    selectAll() {
      this.isCheckAll = !this.isCheckAll;
      this.selected_pipes = [];
      if(this.isCheckAll){ // Check all
        this.selected_pipes = this.rows["result"];
      }
    },
    checkOne() {
      this.selected_option = [];
    },
    checkTestOne() {
      this.selected_test_choice = [];
    },
    scanResponse() {
      api.getResource("/scan_db").then((data) => {
        // eslint-disable-next-line no-console
        //console.log(data)
        if (data != null && data != "") {
          this.isScanResponse = true;
          this.isBufferActive = false;
          this.rows = data;
        }
        if (data['result'] == "Not working") {
            // eslint-disable-next-line no-console
            console.log(data)
            this.rows = "Something didn't work correctly when connecting to your database. Refresh the page and start over."
            this.is404 = true;
            this.isScanResponse = false;
            this.isInputComplete = false;
            this.isBufferActive = false;
        }
      });
    },
    async createDataFlow() {
      let tables = this.selected_pipes;
      this.isScanResponse = false;
      this.isInputComplete = false;
      this.isGlobalBufferActive = true;
      await fetch("http://localhost/backend_autoconnect/create_dataflow", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tables: tables
        }),
      });
      this.sesamResponse();
    },
    sesamResponse() {
      api.getResource("/sesam_response").then((data) => {
        if (data != null && data != "") {
          //eslint-disable-next-line no-console
          //console.log("testing this...");
          //eslint-disable-next-line no-console
          //console.log(data);
          this.isSesamResponse = true;
          this.isGlobalBufferActive = false;
          this.result = data;
        }
      });
    }
  },
};
</script>
  
<style>
select {
  padding: 10%;
  width: 30%;
  height: 40px;
  padding: 5px 10px;
  font-size: 12px;
  color: rgba(0, 0, 0);
  letter-spacing: 1px;
  background: #fff;
  border: 2px solid #fff;
}

input {
  padding: 10%;
  text-align: center;
  width: 40%;
  height: 40px;
  padding: 5px 10px;
  font-size: 12px;
  color: rgba(0, 0, 0);
  letter-spacing: 1px;
  background: #fff;
  border: 2px solid #fff;
}

.center {
  padding: 10%;
}

.sesam {
  padding: 10%;
}

.checkbox_option {
  text-align: center;
  width: 5%;
  background: #fff;
}

.checkbox_select_all {
  width: 5%;
  background: #fff;
  vertical-align: middle;
}

.list_select_all {
  text-align: center;
}

li {
  font-size: 12px;
  text-align: left;
  display: block;
}

.component {
  width: 100%;
  text-align: center;
}

.checkboxes {
  height: 300px;
  overflow-y: scroll;
}
.checkboxes input {
  vertical-align: middle;
}
.checkboxes label span {
  vertical-align: middle;
}

.options {
  font-size: 10px;
}

.options input {
  vertical-align: middle;
}
.options label span {
  vertical-align: middle;
}

.special_button {
  width: 28%;
  padding: 5px 10px;
  font-size: 12px;
  letter-spacing: 1px;
  background: #009fdf;
  height: 40px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #fff;
  -webkit-transition: all 0.1s ease-in-out;
  -moz-transition: all 0.1s ease-in-out;
  -ms-transition: all 0.1s ease-in-out;
  -o-transition: all 0.1s ease-in-out;
  transition: all 0.1s ease-in-out;
}

.left {
  left: 0;
}

.right {
  right: 0;
}

.split {
  height: 100%;
  width: 50%;
  position: fixed;
  z-index: 1;
  top: 20;
  overflow-x: hidden;
  padding-top: 20px;
}

.checkboxes {
  height: 450px;
  overflow-y: scroll;
}
.checkboxes input {
  vertical-align: middle;
}
.checkboxes label span {
  vertical-align: middle;
}

.checkbox_option {
  text-align: center;
  width: 5%;
  background: #fff;
}

.checkbox_select_all {
  width: 5%;
  background: #fff;
  vertical-align: middle;
}

.list_select_all {
  font-size: 12px;
  text-align: center;
  display: block;
}

.list {
  font-size: 12px;
  text-align: left;
  display: block;
}

body {
  background-color: rgb(255, 255, 255);
  box-sizing: border-box;
  color: rgb(61, 57, 53);
  display: block;
  font-family: museo-sans-rounded, sans-serif;
  font-size: 14px;
  font-style: normal;
  height: 720px;
  letter-spacing: 0.2px;
  line-height: 10px;
  margin-bottom: 0px;
  margin-left: 0px;
  margin-right: 0px;
  margin-top: 0px;
  text-size-adjust: 100%;
  width: 100%;
}

</style>