<template>
    
        <form @submit.prevent="createUser" class="container">
                <div class="row offset-md-2">
                    <div class="col-md-3">
                        <label for="inputFirstName" class="form-label">First Name</label>
                        <input type="text" class="form-control" id="inputFirstName" placeholder="Fire Name">
                    </div>
                    <div class="col-md-3">
                        <label for="inputLastName" class="form-label">Last Name</label>
                        <input type="text" class="form-control" id="inputLastName" placeholder="Last Name">
                    </div>
                    <div class="col-md-2">
                        <label for="selectGender" class="form-label">Gender</label>
                        <select class="form-select" id="selectGender">
                            <option selected>Choose...</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="else">Else</option>
                        </select>
                    </div>
                </div>
                <div class="row offset-md-2">
                    <div class="col-md-5">
                        <label for="inputEmail" class="form-label">Email Address</label>
                        <input type="text" class="form-control" id="inputEmail" placeholder="Email Address">
                    </div>
                    <div class="col-md-3">
                        <label for="inputUsername" class="form-label">Username</label>
                        <input type="text" class="form-control" id="inputUsername" placeholder="Username" aria-describedby="basic-addon1">
                    </div>
                </div>
        </form>
</template>

<script>
import axios from "axios"
import useVuelidate from "@vuelidate/core"
import { required, email, minLength, sameAs, or } from "@vuelidate/validators"

export default {
    setup () {
        return { v$: useVuelidate() }
    },
    data () {
        return {
            form: {
                firstName: "",
                lastName: "",
                username: "",
                email: "",
                password: "",
                gender: ""
            },
            confirmedPassword: ""
        }
    },
    methods: {
        createUser: async function() {

            const isValid = await this.v$.validate
            this.form.gender = document.getElementById("selectGender").value

            if (!isValid) {
                console.log("NOT ENOUGH DATA");
                return
            }
            console.log("IS VALID DATA");
            await axios.post("http://127.0.0.1:5000/api/v1/register", this.form)
            // .then(response => {
                
                
            // })
        }
    },
    validations () {
        return {
            firstName:   { required },
            lastName: { required },
            username:  { required },
            email: { 
                required,
                email
            },
            password: { 
                required,
                minLength: minLength(8)
            },
            confirmedPassword: sameAs(this.form.password),
            gender: or("male", "female", "else")
        }
    }
    
}
</script>

<style scoped>


</style>
