<template>
  <div>
    <div class="svgContainer"></div>
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
