<template>
  <div
    v-if="node.children"
    class="node"
  >
    <marker-test v-for="child in node.children" :key="child" :node="child"/>
  </div>
  <div
    v-else
    class="string"
    :style="testColor"
  >
    {{ node.text }}
  </div>
</template>

<script>
export default {
  name: "MarkerTest",
  props: {
    node: Object,
  },
  computed: {
    testColor: function () {
      console.log(this.node.color);
      if (this.node.color) {
        return '--test-color: ' + this.node.color + '4C;';
      }
      return '--test-color: transparent';
    }
  }
}
</script>

<style scoped>

.node {
  display: inline;
}

.node:hover {
  text-decoration:underline;
}

.string{
  background-color: var(--test-color);
  display: inline;
}
</style>
