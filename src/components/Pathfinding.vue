<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="i in playfield.rowCount" :key="i">
            <div v-for="j in playfield.cellCount" :key="j"
                @mousedown="changeCell($event, true)"
                @mouseenter="changeCell($event, false)"
                @mouseup="startCell.selected = false; targetCell.selected = false"
                :class="[   
                    'border-end',
                    'border-bottom',
                    { 'border-top': i === 1 },
                    { 'border-start': j === 1 },
                    'cell',
                    { 'start' : startCell.id === ('row-'+i+'-cell-'+j) },
                    { 'target' : targetCell.id === ('row-'+i+'-cell-'+j) },
                    `hcost=${ (Math.abs(targetCell.row - i) + Math.abs(targetCell.cell - j)) }`
                ]"
                :style="{
                    position: 'fixed', 
                    left: `${21.5 + (j-1) * 2}rem`,
                    top: `${0.5 + (i-1) * 2}rem`,
                    minWidth: '2rem',
                    minHeight: '2rem',
                    }"
                :id="'row-'+i+'-cell-'+j"
                >
                <component 
                v-if="startCell.id === ('row-'+i+'-cell-'+j)"
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
                v-if="targetCell.id === ('row-'+i+'-cell-'+j)"
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
            startCell: {
                id: "",
                row: null,
                cell: null,
                selected: false
            },
            targetCell: {
                id: "",
                row: null,
                cell: null,
                selected: false
            },
            totalCellCount: null,
            timeoutInstance: null,
            intervalInstance: null
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
        changeCell: async function(event, onStart) {

            if (event.buttons !== 1 || this.playfield.running) return
            var cell

            for (let element of event.path) {
                if (element.classList.contains("cell")) {
                    cell = [element.id, element.classList]
                    cell = element
                    break
                }
            }

            if (onStart) {
                if (cell.classList.contains("start")) {
                    this.startCell.selected = true
                }
                else if (cell.classList.contains("target")) {
                    this.targetCell.selected = true
                }
            }
            else {
                if (this.startCell.selected && !cell.classList.contains("obstacle") && !cell.classList.contains("target")) {
                    this.startCell.id = cell.id
                }
                else if (this.targetCell.selected && !cell.classList.contains("obstacle") && !cell.classList.contains("start")) {
                    this.targetCell.id = cell.id
                }
                else if (!this.startCell.selected && !this.targetCell.selected && !cell.classList.contains("start") && !cell.classList.contains("target")) {
                    cell.classList.add("obstacle")
                    cell.style.backgroundColor = "black"
                }
            }
        },
        calculatePlayfieldSize: function(softReset=false) {

            if (softReset) {
                this.softResetPlayfield()
            }
            else {
                this.playfield.rowCount = Math.min(Math.floor(this.window.height / 16 / 2), 40)
                this.playfield.cellCount = Math.floor((this.window.width - 350) / 16 / 2)

                this.startCell.row = Math.floor(this.playfield.rowCount/2)
                this.startCell.cell = Math.floor(this.playfield.cellCount/4)
                this.startCell.id = `row-${this.startCell.row}-cell-${this.startCell.cell}`

                this.targetCell.row = Math.floor(this.playfield.rowCount/2)
                this.targetCell.cell = Math.ceil(this.playfield.cellCount * 0.75) + 1
                this.targetCell.id = `row-${this.targetCell.row}-cell-${this.targetCell.cell}`

                this.totalCellCount = this.playfield.rowCount*this.playfield.cellCount
                this.playfield.pathFound = false
                this.playfield.running = false
                this.renderKey += 1
            }

            return new Promise(resolve => resolve("Success"))
        },
        softResetPlayfield: async function() {

            var obstacles = []
            var startId = this.startCell.id
            this.startCell.row = startId.split("-")[1]
            this.startCell.cell = startId.split("-")[3]

            var targetId = this.targetCell.id
            this.targetCell.row = targetId.split("-")[1]
            this.targetCell.cell = targetId.split("-")[3]

            for (let htmlElement of document.getElementsByClassName("obstacle")) {
                obstacles.push(htmlElement.id)
            }
            this.renderKey += 1
            await this.sleep(0.001)

            for (let id of obstacles) {
                var cell = document.getElementById(id)
                cell.classList.add("obstacle")
                cell.style.backgroundColor = "black"
            }

            this.startCell.id = startId
            this.targetCell.id = targetId
            return
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
        getNeighbours: function(htmlElement, nextNodes, visitedCells, currentNode) {

            var neighbours = [], tempNeighbours = []
            var relativePos = [[0,1], [0,-1], [1,0], [-1,0]]

            relativePos.forEach(pos => {
                let row = htmlElement.id.split("-")[1]
                let cell = htmlElement.id.split("-")[3]
                let neighbour = document.getElementById(`row-${parseInt(row) + pos[0]}-cell-${parseInt(cell) + pos[1]}`)
                if (neighbour) tempNeighbours.push(neighbour)
            })

            tempNeighbours.forEach(neighbour => {
                if (
                    !nextNodes.map(node => { return node.actualCell.id }).includes(neighbour.id)
                    &&
                    !visitedCells.includes(neighbour.id)
                    &&
                    !neighbour.classList.contains("obstacle")
                    ) 
                    {
                        neighbours.push(this.createNode(neighbour, currentNode))
                    }
            })

            return neighbours
        },
        createNode: function(htmlEelement, predecessor) {
            return {
                actualCell: htmlEelement,
                predecessor: predecessor
            }
        },
        colorizeElement: function(htmlEelement) {
            htmlEelement.style.backgroundColor = "rgb(0, 197, 255)"
            htmlEelement.classList.add("visited")
        },
        colorizePath: async function(finalNode) {

            var currentNode = finalNode

            while (currentNode) {
                currentNode.actualCell.style.backgroundColor = "#E6727A"
                currentNode.actualCell.classList.add("finalPath")
                currentNode = currentNode.predecessor
                await this.sleep(0.05)
            }
        },
        startDijkstra: async function(userDelay) {

            this.playfield.running = true
            this.playfield.pathFound = false
            var uniqueRenderKey = this.renderKey

            var startNode = {
                actualCell: document.getElementById(this.startCell.id),
                predecessor: null
            }

            var nextNodes = [startNode]; var visitedCells = []
            
            while (nextNodes.length > 0 && uniqueRenderKey === this.renderKey) {

                var currentNode = nextNodes[0]
                nextNodes.shift()

                this.colorizeElement(currentNode.actualCell)
                await this.sleep((20/parseFloat(userDelay))/this.totalCellCount)

                if (currentNode.actualCell.id === this.targetCell.id) {
                    this.colorizePath(currentNode)
                    break
                }

                var neighbours = this.getNeighbours(currentNode.actualCell, nextNodes, visitedCells, currentNode)

                neighbours.forEach(neighbour => {
                    nextNodes.push(neighbour)
                })
                
                visitedCells.push(currentNode.actualCell.id)
                currentNode = nextNodes[0]
            }

            if (uniqueRenderKey === this.renderKey) {
                this.playfield.running = false
                this.playfield.pathFound = true
            }
        },
        startAStar: async function(userDelay) {

            this.playfield.running = true
            this.playfield.pathFound = false
            var uniqueRenderKey = this.renderKey

            var startCell = document.getElementById(this.startCell.id)
            var currentNode = {
                actualCell: startCell,
                predecessor: null,
                gcost: 0,
                hcost: null,
                fcost: null
            }

            startCell.classList.forEach(classname => {
                if (classname.match(/hcost=[0-9]*/)) {
                    currentNode.hcost = parseInt(classname.split("=")[1])
                    currentNode.fcost = currentNode.gcost + currentNode.hcost
                }
            })

            var possibleNodes = []
            var possibleNodesIds = []
            var fullyVisitedIds = [startCell.id]

            while (currentNode && uniqueRenderKey === this.renderKey) {

                this.colorizeElement(currentNode.actualCell)
                await this.sleep((20/parseFloat(userDelay))/this.totalCellCount)
                fullyVisitedIds.push(currentNode.actualCell.id)

                var relativePos = [[0,1], [0,-1], [1,0], [-1,0]]
                var neighbours = []

                if (currentNode.actualCell.id === this.targetCell.id) {
                    this.colorizePath(currentNode)
                    break
                }

                for (let pos of relativePos) {
                    var currRow = parseInt(currentNode.actualCell.id.split("-")[1])
                    var currCell = parseInt(currentNode.actualCell.id.split("-")[3])
                    var neighbour = document.getElementById(`row-${currRow + pos[0]}-cell-${currCell + pos[1]}`)

                    if (neighbour && !neighbour.classList.contains("obstacle") && !neighbour.classList.contains("visited")) {

                        var hcost; var fcost

                        neighbour.classList.forEach(classname => {
                            if (classname.match(/hcost=[0-9]*/)) {
                                hcost = parseInt(classname.split("=")[1])
                                fcost = currentNode.gcost + hcost + 1
                            }
                        })

                        neighbours.push({
                            actualCell: neighbour,
                            predecessor: currentNode,
                            gcost: currentNode.gcost + 1,
                            hcost: hcost,
                            fcost: fcost
                        })
                    }
                }
                
                neighbours.forEach(neighbour => {
                    
                    if (!possibleNodesIds.includes(neighbour.actualCell.id)) {
                        possibleNodesIds.push(neighbour.actualCell.id)
                        possibleNodes.push(neighbour)
                    }
                    else if (possibleNodesIds.includes(neighbour.actualCell.id) && !fullyVisitedIds.includes(neighbour.actualCell.id)) {
                        for (let node of possibleNodes) {
                            if (node.actualCell.id === neighbour.actualCell.id) {

                                if (neighbour.gcost < node.gcost) {
                                    node.predecessor = neighbour.predecessor
                                    node.gcost = neighbour.gcost
                                    node.fcost = neighbour.fcost
                                }
                            }
                        }
                    }
                })

                var lowestFcost = Math.min(...possibleNodes.map(node => { return node.fcost }))
                var bestNodes = possibleNodes.filter(node => { return node.fcost === lowestFcost})

                if (bestNodes.length === 0) {
                    return
                }
                else if (bestNodes.length === 1) {
                    currentNode = bestNodes[0]
                    possibleNodes.splice(possibleNodes.indexOf(currentNode), 1)
                }
                else if (bestNodes.length > 1) {

                    var lowestHcost = Math.min(...bestNodes.map(node => { return node.hcost} ))
                    var newBestNodes = bestNodes.filter(node => { return node.hcost === lowestHcost })
                    currentNode = newBestNodes[0]
                    possibleNodes.splice(possibleNodes.indexOf(currentNode), 1)
                }
            }

            if (uniqueRenderKey === this.renderKey) {
                this.playfield.running = false
                this.playfield.pathFound = true
            }
        }
    }
}
</script>


<style scoped>

@keyframes visitedCell {
    from {background-color: black;}
    to {background-color: rgb(0, 197, 255);}
}

@keyframes shortestPath {
    from {background-color: #88D8B0;}
    to {background-color: #E6727A;}
}

.visited {
    animation: visitedCell;
    animation-duration: 1s;
}

.finalPath {
    animation: shortestPath;
    animation-duration: 1s;
}

</style>
