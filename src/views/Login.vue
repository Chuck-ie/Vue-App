<template>
    <h3>Loginform: </h3>
    <form v-on:submit.prevent="login">
        <label>Username or Email: </label><input v-model="form.login_name" type="text">
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
                login_name: "",
                password: ""
            }
        }
    },
    methods: {
        login: async function() {
            await axios.post("http://127.0.0.1:5000/api/v1/login", this.form)
                .then(response => {
                    console.log("Process successful login")
                })
                .catch(error => {
                    console.log(error.response)
                    console.log(error.response.data)
                    console.log(error.response.status)
                    console.log(error.response.headers)
                    console.log("handle unsuccessful login fail")
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
