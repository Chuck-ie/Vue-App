<template>
    <h3>Loginform: </h3>
    <form v-on:submit.prevent="login">
        <label>Username or Email:  </label> <input required v-model="form.login_name" type="text">
        <br>
        <label>Password:           </label> <input required v-model="form.password"   type="password">
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
                .catch(error => {
                    console.log("handle unsuccessful login fail")
                    console.log("response",error.response)
                    console.log("data",error.response.data)
                    console.log("status",error.response.status)
                })
                .then(result => {
                    if (result) console.log(result)
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
