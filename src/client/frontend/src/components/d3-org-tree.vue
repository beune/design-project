<template>
  <div style="width: 100vw">
    <v-menu v-model="hintMenuVisible" absolute offset-y :position-x="mouseX" :position-y="mouseY">
    <v-card>
      <v-container v-html="hintMenuContent">
      </v-container>
    </v-card>
    </v-menu>

    <v-menu v-model="contextMenuVisible" absolute offset-y :position-x="mouseX" :position-y="mouseY">
    <!-- TODO: only allow value nodes to be removed. -->
      <v-list dense>
        <v-subheader>OPTIES</v-subheader>
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
          <v-list-item>
            <v-list-item-icon>
              <v-icon>report_off</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Ignore warning</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog v-model="showEditNodeLabelDialog" width="500" >
      <v-card>
        <v-card-title class="headline">
          Label wijzigen
        </v-card-title>
        <v-card-text>
          <v-select v-model="chosenNodeLabelAlternative" :items="nodeLabelAlternatives" label="Label"></v-select>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="showEditNodeLabelDialog = false">Annuleer</v-btn>
          <v-btn color="primary" text @click="editNodeLabel">Wijzigen</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="showNoNodeLabelAlternativesAvailableSnackbar" >
       Er zijn geen alternatieven beschikbaar.
    </v-snackbar>

    <v-container @mousemove="handleMouseMove" class="svgContainer"/>
  </div>
</template>
<style lang="scss">
    .svgContainer {
    /* Because d3-org-tree fits to as much width as possible when a width is not specified, the width is not specified here. */
      height: 86.0vh;
    }
    .domStyle {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;

        * {
            display: inline-block;
            font-weight: bold;
            font-size: 40px;
        }
    }
</style>
<script>
import data from './data.json'
    import OrgTree from "d3-org-tree";
    export default {
        name: "Chart",
        data: () => ({
            hintMenuVisible: false,
            contextMenuVisible: false,

            mouseX: 0,
            mouseY: 0,

            chartReference: null,
            showEditNodeLabelDialog: false,
            showNoNodeLabelAlternativesAvailableSnackbar: false,
            nodeLabelAlternatives: undefined,
            chosenNodeLabelAlternative: undefined,
            currentNodeId: undefined,
            vicinityMargin: 1,
            hintMenuContent: undefined
        }),
        props: {
          treeData: {
            type: Object,
            default: null
          }
        },
        watch: {
            treeData: function(value) {
                this.renderChart(value);
            }
        },
        mounted() {
            this.renderChart(data)
            this.chartReference.transformLayout("left-to-right")
        },
        methods: {
            handleHintMenu() {
              setTimeout(() => {
                if (!this.contextMenuVisible) {
                  this.hintMenuVisible = true
                }
              }, 500)
              let self = this
              data.forEach(function(object){
                if (object.nodeId === self.currentNodeId) {
                  self.hintMenuContent = object.hint
                }
              });
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
              let alternatives;
              data.forEach(function(object){
                if (object.nodeId === self.currentNodeId) {
                  alternatives = object.alternatives
                }
              });
              return alternatives
            },
            toggleEditNodeLabelDialog(){
              //Only show dialog if there are alternatives available. If no alternatives available, show a snackbar that notifies the user.
              this.nodeLabelAlternatives = this.fetchNodeAlternatives()
              if (this.nodeLabelAlternatives.length !== 0){
                this.showEditNodeLabelDialog = !this.showEditNodeLabelDialog;
              }else{
                this.showNoNodeLabelAlternativesAvailableSnackbar = true;
              }
            },
            changeTemplate(nodeId, template){
              data.forEach(function(object){
                if (object.nodeId === nodeId) {
                  object.template = template
                }
              });
            },
            editNodeLabel(){
              this.toggleEditNodeLabelDialog()
              this.changeTemplate(this.currentNodeId,
              "<div class=\"domStyle\"><span>" + this.chosenNodeLabelAlternative.match(/[^(]+/i)[0] + "</div></span><span class=\"material-icons\">mode</span>")
              this.renderChart(data)
              this.chosenNodeLabelAlternative = undefined;
            },
            undoNodeLabelEdit(){
              let self = this
              data.forEach(function(object){
                if (object.nodeId === self.currentNodeId) {
                  object.template = object.originalTemplate
                }
              });
              this.renderChart(data)
            },
            deleteNodeLabel(){
              this.changeTemplate(this.currentNodeId,
              "<div class=\"domStyle\"><span>" + "?" + "</div></span><span class=\"material-icons\">mode</span>")
              this.renderChart(data)
            },
            renderChart(data) {
                if (!this.chartReference) {
                    this.chartReference = new OrgTree();
                }
                this.chartReference
                    .container('.svgContainer')
                    .data(data)
                    .onNodeHover(d => {
                        this.currentNodeId = d
                        this.handleHintMenu()
                    })
                    .onNodeClick(d => {
                        this.contextMenuVisible = true;
                        // Do not show hint menu so that both menus won't overlap.
                        this.hintMenuVisible = false;
                        this.currentNodeId = d
                    })
                    .render();
            }
        }
    }
</script>
