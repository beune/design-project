<template>
  <div
    v-if="node.type === 'node'"
    class="node"
  >
    <v-tooltip
      v-model="show"
      top
    >
      <template slot="activator">
        <span>
          <marker-test v-for="child in node.children" :key="child" :node="child" :parent-callback="display"/>
        </span>
      </template>
      <span>{{ node.label }}</span>
    </v-tooltip>
  </div>
  <div
    v-else
    :class="node.type"
    :style="testColor"
    @mouseover="mouseOver"
    @mouseleave="mouseOver"
  >
    <v-tooltip
      v-model="show"
      top
    >
      <template slot="activator">
        <span>{{ node.text }}</span>
      </template>
      <span>{{ node.label }}</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "MarkerTest",
  props: {
    node: Object,
    parentCallback: Function,
  },
  data: () => ({
    show: false,
  }),
  computed: {
    testColor: function () {
      console.log(this.node.color);
      if (this.node.color) {
        return '--test-color: ' + this.node.color + '4C;';
      }
      return '--test-color: transparent';
    }
  },
  methods: {
    mouseOver: function () {
      if (this.node.type === "other") {
        this.parentCallback();
      } else if (this.node.type === "label") {
        console.log("label")
        this.display();
      }
    },
    display: function () {
      this.show = !this.show;
    }
  }
}
</script>

<style scoped>

.node {
  display: inline;
}

.label {
  background-color: var(--test-color);
  display: inline;
}

.other {
  display: inline;
}

</style>
