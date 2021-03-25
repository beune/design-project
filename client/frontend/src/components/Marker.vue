<template>
  <div
    v-if="node.type === 'node'"
    :class="style_class"
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
    :class="style_class"
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
      if (this.node.color) {
        return '--test-color: ' + this.node.color + '4C;';
      }
      return '--test-color: transparent';
    },
    style_class: function() {
      return this.node.type + (this.show ? " activated" : "");
    }
  },
  methods: {
    mouseOver: function () {
      if (this.node.type === "other") {
        this.parentCallback();
      } else if (this.node.type === "label") {
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
  white-space:pre-wrap;
}

.label {
  background-color: var(--test-color);
  display: inline;
  white-space:pre-wrap;
}

.other {
  display: inline;
  white-space:pre-wrap;
}

.activated {
  text-decoration: underline;
}

</style>
