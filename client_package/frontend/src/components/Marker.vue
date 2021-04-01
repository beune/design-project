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
          <marker-test
            v-for="child in node.children"
            :key="child"
            :node="child"
            :parent-open-callback="display"
            :parent-close-callback="hide"
          />
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
    @mouseleave="mouseLeave"
  >
    <v-tooltip
      v-model="show"
      top
    >
      <template slot="activator">
        <span> {{ node.text }}</span>
      </template>
      <span>{{ node.label }}</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "MarkerTest",
  props: {
    node: {
      type: Object,
      required: true,
    },
    parentOpenCallback: {
      type: Function,
      default: () => {},
    },
    parentCloseCallback: {
      type: Function,
      default: () => {},
    },
  },
  data: () => ({
    show: false,
  }),
  computed: {
    testColor: function () {
      if (this.node.colour) {
        return '--marker-colour: ' + this.node.colour + '4C;';
      }
      return '--marker-colour: transparent';
    },
    style_class: function() {
      return this.node.type + (this.show ? " activated" : "");
    }
  },
  methods: {
    mouseOver: function () {
      if (this.node.type === "other") {
        this.parentOpenCallback();
      } else if (this.node.type === "label") {
        this.display();
      }
    },
    mouseLeave: function () {
      if (this.node.type === "other") {
        this.parentCloseCallback();
      } else if (this.node.type === "label") {
        this.hide();
      }
    },
    display: function () {
      this.show = true;
    },
    hide: function() {
      this.show = false;
    }
  }
}
</script>

<style lang="scss" scoped>

.node {
  display: inline;
  white-space:pre-wrap;
}

.label {
  background-color: var(--marker-colour);
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
