<template>
    <h3>Create an Account:</h3>

    <form v-on:submit.prevent="create_user">
        <label>First Name: </label><input v-model="form.first_name" type="text">
        <br>
        <label>Last Name: <input v-model="form.last_name" type="text"></label>
        <br>
        <label>Username: </label><input v-model="form.username" type="text">
        <br>
        <label>E-Mail Address: </label><input v-model="form.email" type="email">
        <br>
        <label>Password: </label><input v-model="form.password" type="password">
        <br>
        <label>Confirm Password: </label><input type="password">
        <br>
        <button type="submit">Create Account</button>
    </form>

</template>

<script>
import axios from "axios"
export default {
    data () {
        return {
            form: {
                username: "",
                first_name: "",
                last_name: "",
                email: "",
                password: "",
            }
        }
    },
    methods: {
        create_user: async function() {
            await axios.post("http://127.0.0.1:5000/api/v1/register", this.form)
            .then(response => {

                // if (response !=)

                console.log(response)
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
