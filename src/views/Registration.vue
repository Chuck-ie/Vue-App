<template>
    <h3>Create an Account:</h3>

    <form v-on:submit.prevent="create_user">
        <div>First Name:       <input required v-model="form.first_name" type="text">     <p id="first">   </p> </div>
        <div>Last Name:        <input required v-model="form.last_name"  type="text">     <p id="last">    </p> </div> 
        <div>Username:         <input required v-model="form.username"   type="text">     <p id="uname">   </p> </div>
        <div>E-Mail Address:   <input required v-model="form.email"      type="email">    <p id="email">   </p> </div>
        <div>Password:         <input required v-model="form.password"   type="password"> <p id="pw_real"> </p> </div>
        <div>Confirm Password: <input required v-model="pw_confirmation" type="password"> <p id="pw_test"> </p> </div>
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
            },
            pw_confirmation: ""
        }
    },
    methods: {
        create_user: async function() {
            await axios.post("http://127.0.0.1:5000/api/v1/register", this.form)
            // .then(response => {
                
                
            // })
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

p {
    display: inline;
}

</style>
