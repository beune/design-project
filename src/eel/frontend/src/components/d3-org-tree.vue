<template>
        <!--TODO make tree view fit to entire width and height-->
        <div class="svgContainer"></div>
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
            straights: [{text: "straight", value: true}, {text: "curve", value: false}],
            straight: {text: "curve", value: false},
            displayArrow: true,
            straightLink: false,
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
            renderChart(data) {
                if (!this.chartReference) {
                    this.chartReference = new OrgTree();
                }
                this.chartReference
                    .container('.svgContainer')
                    //.svgWidth(800)
                    //.svgHeight(600)
                    .data(data)
                    //.marginLeft(-50)
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
                    //.current('O-2')
                    .displayArrow(this.displayArrow)
                    .straightLink(this.straightLink)
                    .collapsible(false)
                    .onNodeClick(d => {
                        console.log(d + " node clicked")
                    })
                    .onNodeAdd(d => {
                        console.log(d + " node added")
                    })
                    .onNodeRemove(d => {
                        console.log(d + " node removed")
                        this.chartReference.removeNode(d)
                    })
                    .render();


                /*
                //mock trigger click
                setTimeout(() => {
                    d3.select('#O-3').dispatch('click')
                }, 2000)*/

            },

            transformLayout(direction) {
                this.chartReference.transformLayout(direction)
            },

            transformStraightLink(straight) {
                this.chartReference.transformStraightLink(straight)
            },

            toggleArrow(displayArrow) {
                this.chartReference.toggleArrow(displayArrow)
            }
        }
    }

</script>
