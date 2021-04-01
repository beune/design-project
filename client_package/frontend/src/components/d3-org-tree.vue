<template>
  <div style="width: 100vw">
    <v-menu
      v-model="hintMenuVisible"
      absolute
      offset-y
      :position-x="mouseX"
      :position-y="mouseY"
    >
      <v-card>
        <v-container class="show-white-space">
          {{ hintMenuContent }}
        </v-container>
      </v-card>
    </v-menu>

    <v-menu
      v-model="contextMenuVisible"
      absolute
      offset-y
      :position-x="mouseX"
      :position-y="mouseY"
    >
      <!-- TODO: only allow value nodes to be removed. -->
      <v-list dense>
        <v-subheader>OPTIONS</v-subheader>
        <v-list-item @click="deleteNodeLabel">
          <v-list-item-icon>
            <v-icon>delete</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Remove</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="toggleEditNodeLabelDialog">
          <v-list-item-icon>
            <v-icon>mode</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Edit</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="undoNodeLabelEdit">
          <v-list-item-icon>
            <v-icon>undo</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Undo</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-if="uncertain"
          @click="ignoreWarning"
        >
          <v-list-item-icon>
            <v-icon>report_off</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Ignore warning</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog
      v-model="showEditNodeLabelDialog"
      width="500"
    >
      <v-card>
        <v-card-title class="headline">
          Edit label
        </v-card-title>
        <v-card-text>
          <v-select
            v-model="chosenNodeLabelAlternative"
            :items="nodeLabelAlternatives"
            label="Label"
          />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            text
            @click="showEditNodeLabelDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="editNodeLabel"
          >
            Edit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="showNoNodeLabelAlternativesAvailableSnackbar"
    >
      There are no alternatives available.
    </v-snackbar>

    <v-container
      class="svgContainer"
      @mousemove="handleMouseMove"
    />
  </div>
</template>
<style lang="scss">
    .show-white-space {
        white-space: pre-wrap;
    }
    .container.svgContainer {
        width: 100vw;
        max-width: 100vw;
        height: calc(100vh - 90px);
    }
    .domStyle {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;

        * {
            display: inline-block;
            font-size: 40px;
        }
    }
</style>
<script>
    import OrgTree from "d3-org-tree";
    export default {
        name: "Chart",
        props: {
          treeData: {
            type: Array,
            default: null
          }
        },
        data: () => ({
            hintMenuVisible: false,
            contextMenuVisible: false,

            mouseX: 0,
            mouseY: 0,
            uncertain: false,
            chartReference: null,
            showEditNodeLabelDialog: false,
            showNoNodeLabelAlternativesAvailableSnackbar: false,
            nodeLabelAlternatives: undefined,
            chosenNodeLabelAlternative: undefined,
            currentNodeId: undefined,
            vicinityMargin: 1,
            hintMenuContent: undefined,
            mouseHoversOnNode: true
        }),
        computed: {
          chartArrowColor: function () {
            return this.$vuetify.theme.dark ? {
                "red": 255,
                "green": 255,
                "blue": 255,
                "alpha": 1
            } : {
                "red": 45,
                "green": 48,
                "blue": 119,
                "alpha": 1
            }
          },
          // Because you cannot directly watch 'this.$vuetify.theme.dark', I created this field. Hacky, but it workds.
          dark: function(){
            return this.$vuetify.theme.dark
          }
        },
        watch: {
            // Because you cannot directly watch 'this.$vuetify.theme.dark', I created a computed field 'dark'. Hacky, but it workds.
            dark: function () {
              this.renderChart(this.treeData)
            },
            treeData: function(value) {
                this.renderChart(value);
            }
        },
        mounted() {
            this.renderChart(this.treeData)
        },
        methods: {
            handleHintMenu(node) {
              let currentNodeId = this.currentNodeId
              setTimeout(() => {
                if (node.hint != null && !this.contextMenuVisible && this.mouseHoversOnNode && currentNodeId === this.currentNodeId) {
                  this.hintMenuVisible = true
                  this.mouseHoversOnNode = false
                }
              }, 800)
              this.hintMenuContent = node.hint
            },
            handleMouseMove(e){
              let mouseX = e.clientX
              let mouseY = e.clientY
              // If the mouse is not in the vicinity of the the context or hint menu, it will not be visible anymore.
              if (!this.between(this.mouseX, mouseX) && !this.between(this.mouseY, mouseY)){
                this.contextMenuVisible = false
                this.hintMenuVisible = false
              }
              this.mouseX = mouseX
              this.mouseY = mouseY
            },
            between (previous, current) {
              // Tests whether a number is between the specified margin
              return current > previous - this.vicinityMargin && current < previous + this.vicinityMargin
            },
            fetchNodeAlternatives(){
              let self = this
              let alternatives = [];
              this.treeData.forEach(function(object){
                if (object.nodeId === self.currentNodeId && object.alternatives != null) {
                  alternatives = object.alternatives
                }
              });
              return alternatives
            },
            toggleEditNodeLabelDialog(){
              //Only show dialog if there are alternatives available. If no alternatives available, show a snackbar that notifies the user.
              this.nodeLabelAlternatives = this.fetchNodeAlternatives()
              if (this.nodeLabelAlternatives !== null && this.nodeLabelAlternatives.length !== 0){
                this.showEditNodeLabelDialog = !this.showEditNodeLabelDialog;
              }else{
                this.showNoNodeLabelAlternativesAvailableSnackbar = true;
              }
            },
            changeLabel(nodeId, label){
              this.treeData.forEach(function(object){
                if (object.nodeId === nodeId) {
                  object.label = label
                  object.template = "<div class=\"domStyle\"><span>" + label + "</div></span><span class=\"material-icons\">mode</span>"
                }
              });
            },
            editNodeLabel(){
              this.toggleEditNodeLabelDialog()
              let label = this.chosenNodeLabelAlternative
              this.changeLabel(this.currentNodeId, label)
              this.renderChart(this.treeData)
              this.chosenNodeLabelAlternative = undefined;
              window.eel.update_tree(this.currentNodeId, "label", label);
              this.ignoreWarning() //remove warning because of edit
            },
            undoNodeLabelEdit(){
              let self = this
              this.treeData.forEach(function(object){
                if (object.nodeId === self.currentNodeId) {
                  object.template = object.originalTemplate
                  object.lowConfidence = object.originalLowConfidence
                }
              });
              this.renderChart(this.treeData)
              window.eel.update_tree(this.currentNodeId, "label", null);
            },
            deleteNodeLabel(){
              this.changeLabel(this.currentNodeId, "?")
              this.renderChart(this.treeData)
              window.eel.update_tree(this.currentNodeId, "label", "?");
              window.eel.update_tree(this.currentNodeId, "warning", false); //remove warning because of edit
            },
            ignoreWarning(){
              this.treeData.forEach((object) => {
                if (object.nodeId === this.currentNodeId) {
                  object.lowConfidence = false;
                }
              });
              this.renderChart(this.treeData)
              window.eel.update_tree(this.currentNodeId, "warning", false)
            },
            renderChart(data) {
              if (!this.chartReference) {
                  this.chartReference = new OrgTree();
              }
              this.chartReference
                  .container('.svgContainer')
                  .data(data)
                  // Setting backgroundcolor to nothing will make the chart inherit the background color from the app.
                  .backgroundColor()
                  .linkColor(this.chartArrowColor)
                  .onNodeHoverOut(() => {
                      this.mouseHoversOnNode = false
                  })
                  .onNodeHover(d => {
                    this.mouseHoversOnNode = true
                    this.currentNodeId = d.nodeId
                    this.handleHintMenu(d)
                  })
                  .onNodeClick(d => {
                    this.contextMenuVisible = true;
                    let uncert = false
                    this.treeData.forEach(function(object){
                      if (object.nodeId === d.nodeId) {
                        uncert = object.lowConfidence
                      }
                    });
                    this.uncertain = uncert;
                    // Do not show hint menu so that both menus won't overlap.
                    this.hintMenuVisible = false;
                    this.currentNodeId = d.nodeId
                  })
                  .render();
            }
        }
    }
</script>
