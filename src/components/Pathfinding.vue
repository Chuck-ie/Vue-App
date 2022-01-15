<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="i in playfield.rowCount" :key="i">
            <div v-for="j in playfield.cellCount" :key="j"
                @mousemove="changeCell($event)"
                @mouseenter="recomputeAlgo($event)"
                :class="[ 
                    (i-1)+'-'+j+ '|' +i+'-'+(j+1)+ '|' +(i+1)+'-'+j+ '|' +i+'-'+(j-1),
                    'row-'+i+'-cell-'+j,    
                    'border-end',
                    'border-bottom',
                    { 'border-top': i === 1 },
                    { 'border-start': j === 1 },
                    'cell'
                ]"
                :style="{
                    position: 'fixed', 
                    left: `${21.5 + (j-1) * 2}rem`,
                    top: `${0.5 + (i-1) * 2}rem`,
                    minWidth: '2rem',
                    minHeight: '2rem',
                    }"
                :id="(i-1) * playfield.cellCount + j"
                >
                <component 
                :class="['draggable']"
                v-if="(i-1) * playfield.cellCount + j === startCellId"
                :is="'fas'" 
                :icon="'arrow-down'"
                :style="{
                    minWidth: '1.95rem',
                    minHeight: '1.7rem',
                    position: 'relative',
                    top: '0.1rem'
                }"
                >
                </component>
                <component 
                :class="['draggable']"
                v-if="(i-1) * playfield.cellCount + j === targetCellId"
                :is="'fas'" 
                :icon="'bullseye'"
                :style="{
                    minWidth: '1.95rem',
                    minHeight: '1.7rem',
                    position: 'relative',
                    top: '0.1rem'
                }"
                >
                </component>
            </div>
        </div>
    </div>
</template>

<script>
import { useWindowSize } from "vue-window-size"

export default {
    data() {
        var { width, height } = useWindowSize();
        return {
            renderKey: 0,
            window: {
                width: width,
                height: height
            },
            playfield: {
                rowCount: null,
                cellCount: null,
                running: false,
                timeout: null,
                pathFound: false,
                solvingSpeed: 0
            },
            startCellId: null,
            targetCellId: null,
            totalCellCount: null
        }
    },
    mounted() {
        this.calculatePlayfieldSize()
        window.addEventListener("resize", () => {

            clearTimeout(this.playfield.timeout)
            this.playfield.timeout = setTimeout(() => {
                this.calculatePlayfieldSize()
            }, 150)
        })
    },
    methods: {
        changeCell: function(event) {

            var x = event.x; var y = event.y
            var elementsAtCursor = document.elementsFromPoint(x, y)

            for (var element of elementsAtCursor) {
                if (element.classList.contains("cell") && !element.classList.contains("obstacle") && parseInt(element.id) !== this.startCellId && parseInt(element.id) !== this.targetCellId) {

                    if (event.altKey && !this.playfield.running) {
                        element.style.backgroundColor = "black"
                        element.classList.add("obstacle")
                    }
                    else if (event.shiftKey && !this.playfield.running && !this.playfield.pathFound) {
                        this.startCellId = parseInt(element.id)
                    }
                    else if (event.ctrlKey && !this.playfield.running && !this.playfield.pathFound) {
                        this.targetCellId = parseInt(element.id)
                    }
                }
            }
        },
        calculatePlayfieldSize: function() {
            this.playfield.rowCount = Math.min(Math.floor(this.window.height / 16 / 2), 40)
            this.playfield.cellCount = Math.floor((this.window.width - 350) / 16 / 2)
            this.startCellId = (Math.ceil(this.playfield.rowCount / 2) - 1) * (this.playfield.cellCount) + Math.floor(this.playfield.cellCount / 4)
            this.targetCellId = (Math.ceil(this.playfield.rowCount / 2) - 1) * (this.playfield.cellCount) + Math.ceil((this.playfield.cellCount / 4) * 3) + 1
            this.totalCellCount = this.playfield.rowCount*this.playfield.cellCount
            this.playfield.pathFound = false
            this.playfield.running = false
            this.renderKey += 1

            return new Promise(resolve => resolve("Success"))
        },
        sleep: function(seconds) {

            return new Promise((resolve, reject) => {
                var promise = setTimeout(() => {
                    resolve("Success")
                }, seconds * 1000)

                if (!promise) {
                    reject("Something weird happened.")
                }
            });
        },
        colorize: function(element, color) {

            switch(color) {
                case "yellow":
                    element.style.backgroundColor = "#FFEEAD"
                    break

                case "red":
                    element.style.backgroundColor = "#FF6F69"
                    break
            }
        },
        getNeighbours: function(element) {

            var neighbours = []
            element.classList[0].split("|").forEach(row_cell => {
                var newNeighbour = document.getElementsByClassName(`row-${row_cell.split("-")[0]}-cell-${row_cell.split("-")[1]}`)[0]
                if (newNeighbour) neighbours.push(newNeighbour)
            })

            return neighbours
        },
        createNode: function(element, predecessor) {
            return {
                actualCell: element,
                predecessor: predecessor
            }
        },
        colorizePath: async function(finalNode) {

            var currentNode = finalNode
            while (currentNode) {
                currentNode.actualCell.style.backgroundColor = "#88D8B0"
                currentNode.actualCell.classList.add("finalPath")
                currentNode = currentNode.predecessor
            }
        },
        recomputeAlgo: async function(event) {

            var x = event.x; var y = event.y
            var elementsAtCursor = document.elementsFromPoint(x, y)

            for (var element of elementsAtCursor) {
                if (element.classList.contains("cell") && !element.classList.contains("obstacle") && parseInt(element.id) !== this.startCellId && parseInt(element.id) !== this.targetCellId) {

                    var startId; var targetId
                    if (event.shiftKey && !this.playfield.running && this.playfield.pathFound) {
                        startId = parseInt(element.id)
                        targetId = this.targetCellId

                        await this.calculatePlayfieldSize()

                        this.startCellId = startId; this.targetCellId = targetId
                        this.startDijkstra(0, false)
                    }
                    else if (event.ctrlKey && !this.playfield.running && this.playfield.pathFound) {
                        this.playfield.running = true
                        targetId = parseInt(element.id)
                        startId = this.startCellId

                        await this.calculatePlayfieldSize()

                        this.startCellId = startId; this.targetCellId = targetId
                        this.startDijkstra(0, false)
                    }

                }
            }
        },
        startDijkstra: async function(userDelay, computationDelay=true) {

            this.playfield.running = true
            var uniqueRenderKey = this.renderKey

            var startNode = this.createNode(document.getElementById(this.startCellId), null)
            var targetNode = this.createNode(document.getElementById(this.targetCellId), undefined)

            var nextNodes = [startNode]; var visitedNodes = []
            
            while (this.playfield.pathFound !== true && nextNodes.length > 0) {

                if (uniqueRenderKey !== this.renderKey) return
                var currentNode = nextNodes[0]
                nextNodes.shift()

                this.colorize(currentNode.actualCell, "yellow")
                if (computationDelay) await this.sleep((20/parseFloat(userDelay))/this.totalCellCount)

                if (currentNode.actualCell === targetNode.actualCell) {
                    targetNode.predecessor = currentNode
                    this.playfield.pathFound = true
                    this.colorizePath(targetNode)
                    break
                }

                this.colorize(currentNode.actualCell, "red")
                var newNeighbours = this.getNeighbours(currentNode.actualCell)

                newNeighbours.forEach(neighbour => {
                    if (
                        !nextNodes.map(node => { return node.actualCell }).includes(neighbour)
                        &&
                        !visitedNodes.map(node => { return node.actualCell }).includes(neighbour)
                        ) {
                            nextNodes.push(this.createNode(neighbour, currentNode))
                        }
                })
                
                visitedNodes.push(currentNode)
                currentNode = nextNodes[0]
            }

            this.playfield.running = false
        },
        startAStar: function() {
        }
    }
}
</script>


<style scoped>

.finalPath {
    animation-name: fadeIn;
    animation-duration: 0.4s;
}

@keyframes fadeIn {
    from {background-color: #FF6F69}
    to {background-color: #88D8B0}
}

</style>
