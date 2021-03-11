<template>
  <div style="width: 100vw">
    <v-menu
      v-model="contextMenuVisible"
      absolute
      offset-y
      :position-x="contextMenuX"
      :position-y="contextMenuY"
    >
    <!-- TODO: when the user clicks away from the menu, the menu flashes where the user has clicked. Prevent this. -->
    <v-list dense>
      <v-subheader>OPTIES</v-subheader>
        <v-list-item>
          <v-list-item-icon>
            <v-icon>delete</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Remove</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-icon>
            <v-icon>mode</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Edit</v-list-item-title>
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
    <v-container @click="getClickCoordinates" class="svgContainer"/>
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
            contextMenuVisible: false,
            contextMenuX: 0,
            contextMenuY: 0,
            chartReference: null,
            displayArrow: true,
            straightLink: false,
            showEditNodeLabelDialog: false,
            nodeLabelAlternatives: undefined,
            chosenNodeLabelAlternative: undefined,
            clickedNodeId: undefined
        }),
        watch: {
            data(value) {
                this.renderChart(value);
            }
        },
        mounted() {
            this.renderChart(data)
            this.chartReference.transformLayout("left-to-right")
        },
        methods: {
            toggleContextMenu () {
                this.contextMenuVisible = !this.contextMenuVisible;
            },
            getClickCoordinates (e) {
              this.contextMenuX = e.clientX
              this.contextMenuY = e.clientY
            },
            fetchNodeAlternatives(){
              let self = this
              let alternatives;
              data.forEach(function(object){
                if (object.nodeId === self.clickedNodeId) {
                  alternatives = object.alternatives
                }
              });
              return alternatives
            },
            toggleEditNodeLabelDialog(){
              this.showEditNodeLabelDialog = !this.showEditNodeLabelDialog;
            },
            editNodeLabel(){
              this.toggleEditNodeLabelDialog()
              let self = this
              data.forEach(function(object){
                if (object.nodeId === self.clickedNodeId) {
                  object.template = "<div class=\"domStyle\">\n<span>" + self.chosenNodeLabelAlternative + "</span></div>"
                }
              });
              this.renderChart(data)
              this.chosenNodeLabelAlternative = undefined;
            },
            renderChart(data) {
                if (!this.chartReference) {
                    this.chartReference = new OrgTree();
                }
                this.chartReference
                    .container('.svgContainer')
                    .data(data)
                    .backgroundColor('#ffffff')
                    .highlight({
                        "borderWidth": 1,
                        "borderRadius": 15,
                        "borderColor": {
                            "red": 70,
                            "green": 130,
                            "blue": 180,
                            "alpha": 1
                        },
                        "backgroundColor": {
                            "red": 70,
                            "green": 130,
                            "blue": 180,
                            "alpha": 1
                        }
                    })
                    .duration(0)
                    .displayArrow(this.displayArrow)
                    .straightLink(this.straightLink)
                    .collapsible(false)
                    .onNodeClick(d => {
                        this.toggleContextMenu()
                        this.clickedNodeId = d;
                        this.nodeLabelAlternatives = this.fetchNodeAlternatives()
                        if (this.nodeLabelAlternatives.length !== 0){
                          this.toggleEditNodeLabelDialog();
                        }
                    })
                    .onNodeAdd(d => {
                        console.log(d + " node added")
                    })
                    .onNodeRemove(d => {
                        console.log(d + " node removed")
                        this.chartReference.removeNode(d)
                    })
                    .render();
            }
        }
    }
</script>
