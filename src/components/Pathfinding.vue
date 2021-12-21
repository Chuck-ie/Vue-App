<template>
    <h3>hi from pathing</h3>

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
                running: false,
                timeout: null
            }
        }
    },
    methods: {
        hi: function() {
            console.log("HI FROM PATHING");
        }
    }
}


</script>


<style scoped>

h3 {
    text-align: center;
}

</style>
