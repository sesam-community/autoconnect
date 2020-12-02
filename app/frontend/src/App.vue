<template>
  <div id="app">
    <div>
      <div class="header">
        <Header />
      </div>
      <br />
      <NewIndex />
      <Footer />
    </div>
    
  </div>
</template>

<script>
import NewIndex from "./components/NewIndex.vue";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "app",
  components: {
    NewIndex,
    Header,
    Footer,
  },
  
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.header {
  background-color: rgb(61, 57, 53);
  content: "";
  position: absolute;
  height: 70px;
  top: 0;
  right: 0;
  left: 0;
  z-index: 1;
}

</style>
