<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="elementId in playfield.elementIds" :key="elementId">
            <div
                :class="[
                    'list-group-item',
                    'list-group-item-dark',
                    'sortingElement'
                ]"
                :id="[elementId]"
                :style="{
                    position: 'fixed',
                    minWidth: '1.8rem',
                    minHeight: `${playfield.elementHeight * elementId + playfield.elementHeight}px`,
                    left: `${24 + playfield.elementIds.indexOf(elementId) * 2.6}rem`,
                }">
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
            window: {
                width: width,
                height: height
            },
            playfield: {
                elementIds: null,
                elementHeight: 0,
                running: false,
                timeout: null,
                isSorted: false,
                solvingSpeed: 0
            },
            renderKey: 0
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
        calculatePlayfieldSize: function() {
            
            var arrayLength = Math.floor((this.window.width - 450) / 16 / 2.6)
            this.playfield.elementIds = []
            this.playfield.running = false
            this.playfield.isSorted = false
            
            for (var i = 0; i < arrayLength; i++) {
                this.playfield.elementIds.push(i)
            }

            this.playfield.elementIds.sort(() => Math.random() - 0.5)
            this.playfield.elementHeight = Math.floor((this.window.height - 400) / arrayLength)
            this.renderKey += 1
        },
        sleep: function(seconds) {

            return new Promise((resolve, reject) => {
                var promise = setTimeout(() => {
                    resolve("Success")
                }, seconds * 1000)

                if (!promise) {
                    reject("Something weird happend.")
                }
            });
        },
        calculateDelay: function(x, y) {
            
            var averageDelay = 20/(x ** 2 + x)
            this.playfield.solvingSpeed = averageDelay / parseFloat(y)
        },
        colorize: function(element, newColor) {

            // newColor parameter is not actually a color, but a bootstrap class
            // classname definitions: dark = grey; primary = blue; warning = yellow; danger = red; success = green
            var currentColor = element.classList[1].split("-")[3]
            element.classList.replace(`list-group-item-${currentColor}`, `list-group-item-${newColor}`)
        },
        swapElements: function(element1, element2) {
            
            [element1.id, element2.id] = [element2.id, element1.id];
            [element1.style.minHeight, element2.style.minHeight] = [element2.style.minHeight, element1.style.minHeight]
        },
        startSelectionSort: async function(userMultiplier) {

            var allElements = Array.from(document.getElementsByClassName("sortingElement"))
            this.calculateDelay(parseInt(allElements.length), userMultiplier)
            this.playfield.running = true

            for (var selectedElement of allElements) {

                var bestElement = selectedElement
                var slicedArray = allElements.slice(allElements.indexOf(selectedElement) + 1)
                this.colorize(selectedElement, "primary")

                for (var compareElement of slicedArray) {

                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(compareElement, "warning")

                    await this.sleep(this.playfield.solvingSpeed)
                    if (parseInt(compareElement.id) < parseInt(bestElement.id)) {

                        if (bestElement !== selectedElement) {
                            this.colorize(compareElement, "success")
                            this.colorize(bestElement, "danger")
                        } else {
                            this.colorize(compareElement, "success")
                        }
                        bestElement = compareElement

                    } else {
                        this.colorize(compareElement, "danger")
                    }
                }
                await this.sleep(this.playfield.solvingSpeed)
                
                if (bestElement !== selectedElement) {
                    this.swapElements(selectedElement, bestElement)
                    this.colorize(selectedElement, "success")
                    this.colorize(bestElement, "primary")

                } else {
                    this.colorize(selectedElement, "success")
                }
                
                await this.sleep(this.playfield.solvingSpeed)
                for (var element of slicedArray) {
                    this.colorize(element, "dark")
                }
            }

            if (document.body.contains(allElements[0])) {
                this.playfield.running = false
                this.playfield.isSorted = true
                return
            }
        },
        startQuickSort: async function(userMultiplier) {

            var allElements = Array.from(document.getElementsByClassName("sortingElement"))
            this.playfield.running = true

            this.calculateDelay(parseInt(allElements.length), userMultiplier)
            await this.quickSort(allElements, 0, allElements.length-1)
            
            if (document.body.contains(allElements[0])) {
                this.playfield.running = false
                this.playfield.isSorted = true
                return
            }
        },
        quickSort: async function(array, low, high) {
            
            if (low < high) {

                var split = await this.quickSortParter(array, low, high)
                await this.quickSort(array, low, split - 1)
                await this.quickSort(array, split + 1, high)

            } else if (low === high) {
                this.colorize(array[low], "success")
                this.sleep(this.playfield.solvingSpeed)
            }
        },
        quickSortParter: async function(array, low, high) {

            let pivot = high
            let i = low
            let j = high-1

            this.colorize(array[pivot], "primary")
            this.colorize(array[i], "warning")
            this.colorize(array[j], "danger")
            await this.sleep(this.playfield.solvingSpeed)

            while (i < j) {

                while (i < high && parseInt(array[i].id) < parseInt(array[pivot].id)) {
                    i++
                    this.colorize(array[i - 1], "dark")
                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(array[i], "warning")
                    await this.sleep(this.playfield.solvingSpeed)
                }

                while (j > low && parseInt(array[j].id) > parseInt(array[pivot].id)) {
                    j--
                    this.colorize(array[j + 1], "dark")
                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(array[j], "danger")
                    await this.sleep(this.playfield.solvingSpeed)
                }

                if (i < j) {
                    this.swapElements(array[i], array[j])
                }
            }

            if (parseInt(array[i].id) > parseInt(array[pivot].id)) {
                this.swapElements(array[i], array[high])
            }

            this.colorize(array[i], "success")
            await this.sleep(this.playfield.solvingSpeed)

            var unsortedElements = array.filter(element => {
                return element.classList[1] !== "list-group-item-success"
            })

            for (var element of unsortedElements) {
                this.colorize(element, "dark")
            }

            return i
        },
        startBubbleSort: async function(userMultiplier) {

            var allElements = Array.from(document.getElementsByClassName("sortingElement"))
            this.calculateDelay(parseInt(allElements.length), userMultiplier)

            this.playfield.running = true

            for (let i = 1; i < allElements.length; i++) {
                for (let j = i; j > 0; j--) {

                    var highElement = allElements[j]
                    var lowElement = allElements[j-1]

                    this.colorize(highElement, "warning")
                    this.colorize(lowElement, "warning")
                    await this.sleep(2 * this.playfield.solvingSpeed)

                    if (parseInt(highElement.id) < parseInt(lowElement.id)) {
                        this.swapElements(highElement, lowElement)

                        this.colorize(highElement, "success")
                        this.colorize(lowElement, "success")
                        await this.sleep(2 * this.playfield.solvingSpeed)
                    }
                    else {
                        this.colorize(highElement, "danger")
                        this.colorize(lowElement, "danger")
                        await this.sleep(2 * this.playfield.solvingSpeed)
                    }
                }

                if (i+1 < allElements.length) {
                    for (var element of allElements) {
                        this.colorize(element, "dark")
                    }
                    await this.sleep(2 * this.playfield.solvingSpeed)
                }
            }

            if (document.body.contains(allElements[0])) {
                this.playfield.running = false
                this.playfield.isSorted = true
                return
            }
        },
        startRadixSort: async function(userMultiplier) {

            var allElements = Array.from(document.getElementsByClassName("sortingElement"))
            var currentOrder = allElements.map(element => { return element.id })
            var currRenderKey = this.renderKey

            this.calculateDelay(parseInt(allElements.length), userMultiplier)

            this.playfield.running = true
            var counter = 0
            var maxNumLength = (allElements.length - 1).toString().length

            while (counter < maxNumLength) {

                var newOrder = []

                for (var digit = 0; digit <= 9; digit++) {
                    for (let id of currentOrder) {

                        var comparisonDigit = id.charAt(id.length - counter - 1)
                        if ((comparisonDigit && comparisonDigit == digit) || !comparisonDigit && digit === 0) newOrder.push(id)
                    }
                }

                for (var i = 0; i < allElements.length; i++) {

                    var element1 = document.getElementById(currentOrder[i])
                    var element2 = document.getElementById(newOrder[i])

                    this.colorize(element1, "warning")
                    this.colorize(element2, "warning")
                    await this.sleep(4*this.playfield.solvingSpeed)

                    if (this.renderKey !== currRenderKey) {
                        this.colorize(element1, "dark")
                        this.colorize(element2, "dark")
                        return
                    }
                    this.swapElements(element1, element2)

                    this.colorize(element1, "success")
                    this.colorize(element2, "success")
                    await this.sleep(4*this.playfield.solvingSpeed)


                    if (counter === maxNumLength-1 && element1.id != element2.id) {
                        this.colorize(element1, "success")
                        this.colorize(element2, "dark")
                    }
                    else if (counter === maxNumLength-1 && element1.id == element2.id) {
                        this.colorize(element1, "dark")
                        this.colorize(element2, "success")
                    }
                    else {
                        this.colorize(element1, "dark")
                        this.colorize(element2, "dark")
                    }

                    let [id, j] = [currentOrder[i], currentOrder.indexOf(newOrder[i])]
                    currentOrder[i] = newOrder[i]
                    currentOrder[j] = id
                }

                currentOrder = newOrder
                counter++
            }

            this.playfield.running = false
            this.playfield.isSorted = true
        }
    }
}


</script>

<style scoped>

@keyframes fadeIn {
    from {
        min-height: 0;
    };
    to {
        min-height: 100%;
    }
}

.sortingElement {
    animation: fadeIn 1s;
}

</style>
