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
        <v-list-item @click="toggleEditNodeLabelDialog">
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
            showNoNodeLabelAlternativesAvailableSnackbar: false,
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
              //Only show dialog if there are alternatives available. If no alternatives available, show a snackbar that notifies the user.
              this.nodeLabelAlternatives = this.fetchNodeAlternatives()
              if (this.nodeLabelAlternatives.length !== 0){
                this.showEditNodeLabelDialog = !this.showEditNodeLabelDialog;
              }else{
                this.showNoNodeLabelAlternativesAvailableSnackbar = true;
              }
            },
            editNodeLabel(){
              this.toggleEditNodeLabelDialog()
              let self = this
              data.forEach(function(object){
                if (object.nodeId === self.clickedNodeId) {
                  object.template = "<div class=\"domStyle\">\n<span>" + self.chosenNodeLabelAlternative + "</div></span><span class=\"material-icons\">mode</span>"
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
