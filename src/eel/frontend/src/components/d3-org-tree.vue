<template>
        <!--TODO make tree view fit to entire width and height-->
        <div>
          <div class="svgContainer"></div>
          <md-dialog :md-active.sync="showEditNodeLabelDialog">
            <md-dialog-title>Label wijzigen</md-dialog-title>
            <md-dialog-content>
              <md-field>
                <label>Label</label>
                <!--https://github.com/vuematerial/vue-material/issues/2285 -->
                <md-select v-model="chosenNodeLabelAlternative">
                  <md-option v-for="alternative in nodeLabelAlternatives" :key="alternative" :value="alternative">{{ alternative }}</md-option>
                </md-select>
              </md-field>
            </md-dialog-content>
            <md-dialog-actions>
              <md-button class="md-primary" @click="showEditNodeLabelDialog = false">Annuleer</md-button>
              <md-button class="md-primary" @click="editNodeLabel">Opslaan</md-button>
            </md-dialog-actions>
          </md-dialog>
        </div>
</template>
<style lang="scss">
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
            chartReference: null,
            displayArrow: true,
            straightLink: false,
            showEditNodeLabelDialog: false,
            nodeLabelAlternatives: ["Circumscribed", "Microlobulated", "Indistinct", "Spiculated"],
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
                            "red": 50,
                            "green": 255,
                            "blue": 30,
                            "alpha": 1
                        },
                        "backgroundColor": {
                            "red": 20,
                            "green": 100,
                            "blue": 40,
                            "alpha": 1
                        }
                    })
                    .duration(0)
                    .displayArrow(this.displayArrow)
                    .straightLink(this.straightLink)
                    .collapsible(false)
                    .onNodeClick(d => {
                        this.toggleEditNodeLabelDialog();
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
