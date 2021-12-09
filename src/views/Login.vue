<template>
    <h3>Loginform: </h3>
    <form v-on:submit.prevent="login">
        <label>Username: </label><input v-model="form.username" type="text">
        <br>
        <label>Password: </label><input v-model="form.password" type="password">
        <br>
        <button type="submit">Login</button>
    </form>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            form: {
                username: "",
                password: ""
            }
        }
    },
    methods: {
        login: async function() {
            await axios.post("http://127.0.0.1:5000/api/login", this.form)
            .then(test => {
                console.log("Status 200", test)
            })
        }
    }
}
</script>

<style scoped>

form {
    display: inline-block;
    width: 250px;
    text-align: left;
}

input {
    display: inline-block;
}

</style>
