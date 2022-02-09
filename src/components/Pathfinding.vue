<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="i in playfield.rowCount" :key="i">
            <div v-for="j in playfield.cellCount" :key="j"
                @mousedown="changeCell($event)"
                @mousemove="changeCell($event)"
                @mouseup="startCell.selected = false; targetCell.selected = false"
                @touchmove="changeCell($event)"
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

        document.getElementsByTagName("html")[0].setAttribute("draggable", false)

        this.calculatePlayfieldSize()
        window.addEventListener("resize", () => {

            clearTimeout(this.playfield.timeout)
            this.playfield.timeout = setTimeout(() => {
                this.calculatePlayfieldSize()
            }, 150)
        })
    },
    methods: {
        changeCell: async function(event) {

            if (event.buttons !== 1) return
            var cell

            for (let element of event.path) {
                if (element.classList.contains("cell")) {
                    cell = [element.id, element.classList]
                    cell = element
                    break
                }
            }

            if (this.startCell.selected && !cell.classList.contains("target")) {
                this.startCell.id = cell.id
                return
            }
            else if (this.targetCell.selected && !cell.classList.contains("start")) {
                this.targetCell.id = cell.id
                return
            }

            if (!cell.classList.contains("obstacle") && !cell.classList.contains("start") && !cell.classList.contains("target") && !this.playfield.running) {
                cell.classList.add("obstacle")
                cell.style.backgroundColor = "black"
            }
            else if (!cell.classList.contains("obstacle") && cell.classList.contains("start") && !cell.classList.contains("target") && !this.playfield.running) {
                this.startCell.selected = true
                this.targetCell.selected = false
            }
            else if (!cell.classList.contains("obstacle") && !cell.classList.contains("start") && cell.classList.contains("target") && !this.playfield.running) {
                this.targetCell.selected = true
                this.startCell.selected = false
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
            var targetId = this.targetCell.id

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
        colorizeNode: function(htmlEelement) {
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
            var uniqueRenderKey = this.renderKey

            var startNode = this.createNode(document.getElementById(this.startCell.id), null)
            var targetNode = this.createNode(document.getElementById(this.targetCell.id), undefined)
            var nextNodes = [startNode]; var visitedCells = []
            
            while (nextNodes.length > 0 && uniqueRenderKey == this.renderKey) {

                var currentNode = nextNodes[0]
                nextNodes.shift()

                this.colorizeNode(currentNode.actualCell)
                await this.sleep((20/parseFloat(userDelay))/this.totalCellCount)

                if (currentNode.actualCell === targetNode.actualCell) {
                    targetNode.predecessor = currentNode
                    this.colorizePath(targetNode)
                    break
                }

                var neighbours = this.getNeighbours(currentNode.actualCell, nextNodes, visitedCells, currentNode)

                neighbours.forEach(neighbour => {
                    nextNodes.push(neighbour)
                })
                
                visitedCells.push(currentNode.actualCell.id)
                currentNode = nextNodes[0]
            }

            this.playfield.running = false
            this.playfield.pathFound = true
        },
        startAStar: async function(userDelay) {

            this.playfield.running = true
            var uniqueRenderKey = this.renderKey

            var startNode = this.createNode(document.getElementById(this.startCell.id), null)
            var targetNode = this.createNode(document.getElementById(this.targetCell.id), undefined)
            var visitedCells = [startNode.actualCell.id]; var possibleNodes = []
            var currentNode = startNode
            
            while (possibleNodes.length > 0 || currentNode !== null && uniqueRenderKey === this.renderKey) {

                visitedCells.push(currentNode.actualCell.id)
                this.colorizeNode(currentNode.actualCell)
                await this.sleep((20/parseFloat(userDelay))/this.totalCellCount)

                if (currentNode.actualCell === targetNode.actualCell) {
                    targetNode.predecessor = currentNode
                    this.playfield.pathFound = true
                    this.colorizePath(targetNode)
                    break
                }

                var neighbours = this.getNeighbours(currentNode.actualCell, possibleNodes, visitedCells, currentNode)

                neighbours.map(neighbour => {
                    
                    var gcost = 0
                    var hcost
                    for (let classname of neighbour.actualCell.classList.values()) {
                        if (classname.match(/hcost=[0-9]*/)) hcost = parseInt(classname.split("=")[1])
                    }

                    var temp = neighbour.actualCell
                    while (temp) {
                        temp = temp.predecessor
                        gcost += 1
                    }

                    return Object.assign(neighbour, {
                        gcost: gcost,
                        hcost: hcost,
                        fcost: gcost + hcost
                    })
                }).forEach(node => {
                    possibleNodes.push(node)
                })

                var bestWeighting = Math.min(...possibleNodes.map(node => {
                    return node.fcost
                }))

                var bestNeighbours = possibleNodes.filter(node => {
                    return node.fcost === bestWeighting
                })

                if (bestNeighbours.length === 0) {
                    currentNode = null
                }
                else if (bestNeighbours.length === 1) {
                    currentNode = bestNeighbours[0]
                    possibleNodes.splice(possibleNodes.indexOf(currentNode), 1)
                }
                else if (bestNeighbours.length > 1) {

                    var bestHcost = Math.min(...bestNeighbours.map(node => {
                        return node.hcost
                    }))

                    currentNode = bestNeighbours.filter(neighbour => {
                        return neighbour.hcost === bestHcost
                    })[0]
                    
                    possibleNodes.splice(possibleNodes.indexOf(currentNode), 1)
                }
            }

            this.playfield.running = false
            this.playfield.pathFound = true
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
