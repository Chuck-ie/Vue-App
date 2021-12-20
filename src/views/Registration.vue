<template>
    <h3>Create Your Account:</h3>
    <br>
    <br>
    <br>
    <br>
    <form class="container" @submit.prevent="createUser" novalidate>
        <div class="row offset-md-3 needs-validation">
            <div class="col-md-4">
                <label for="inputFirstName" class="form-label">First Name</label>
                <input v-model="form.firstName" type="text" class="form-control" id="inputFirstName" placeholder="First Name"
                v-bind:class="{
                    'is-valid': !v$.form.firstName.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.firstName.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.firstName.$invalid">
                    Please enter your first name!
                </div>
            </div>
            <div class="col-md-4">
                <label 
                    for="inputLastName" class="form-label">Last Name</label>
                <input v-model="form.lastName" type="text" class="form-control" id="inputLastName" placeholder="Last Name"
                v-bind:class="{
                    'is-valid': !v$.form.lastName.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.lastName.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.lastName.$invalid">
                    Please enter your last name!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-3">
            <div class="col-md-8">
                <label for="inputEmail" class="form-label">Email Address</label>
                <input v-model="form.email" type="text" class="form-control" id="inputEmail" placeholder="Email Address"
                v-bind:class="{
                    'is-valid': !v$.form.email.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.email.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.email.required.$invalid">
                    Please enter your email address!
                </div>
                <div class="invalid-feedback" v-else-if="v$.form.email.email.$invalid">
                    Please enter a valid email format!
                </div>
                <div id="email-exists" class="invalid-feedback">
                    Email address already exists!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-3">
            <div class="col-md-4">
                <label for="inputUsername" class="form-label">Username</label>
                <input v-model="form.username" type="text" class="form-control" id="inputUsername" placeholder="Username"
                v-bind:class="{
                    'is-valid': !v$.form.username.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.username.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.username.$invalid">
                    Please enter a username!
                </div>
                <div id="username-exists" class="invalid-feedback">
                    Username already exists!
                </div>
            </div>
            <div class="col-md-4">
                <label for="selectGender" class="form-label">Gender</label>
                <select v-model="form.gender" class="form-select" id="selectGender" aria-placeholder="Choose..."
                v-bind:class="{
                    'is-valid': !v$.form.gender.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.gender.$invalid && v$.form.$dirty
                    }"
                >
                    <option value="" selected>Choose...</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="else">Else</option>
                </select>
                <div class="invalid-feedback" v-if="v$.form.gender.$invalid">
                    Please select a gender!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-3">
            <div class="col-md-4">
                <label for="inputPassword" class="form-label">Password</label>
                <input v-model="form.password.password" type="password" class="form-control" id="inputPassword" placeholder="Password"
                v-bind:class="{
                    'is-valid': !v$.form.password.password.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.password.password.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.password.password.required.$invalid">
                    Please enter a password!
                </div>
                <div class="invalid-feedback" v-else-if="v$.form.password.password.minLength.$invalid">
                    Password needs at least 8 Characters!
                </div>
            </div>
            <div class="col-md-4">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input v-model="form.password.confirmed" type="password" class="form-control" id="confirmPassword" placeholder="Confirm Password"
                v-bind:class="{
                    'is-valid': !v$.form.password.confirmed.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.password.confirmed.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.password.confirmed.required.$invalid">
                    Please enter a password!
                </div>
                <div class="invalid-feedback" v-else-if="v$.form.password.confirmed.sameAsPassword.$invalid">
                    Your passwords don't match!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-3">
            <div class="col-md-4">
                <button type="submit" class="btn btn-outline-success">Create Account</button>
            </div>
        </div>
        <br>
    </form>
</template>

<script>
import axios from "axios"
import useVuelidate from "@vuelidate/core"
import { required, minLength, sameAs, email } from "@vuelidate/validators"

export default {
    data() {
        return {
            v$: useVuelidate(),
            form: {
                firstName: "",
                lastName: "",
                username: "",
                email: "",
                password: {
                    password: "",
                    confirmed: ""
                },
                gender: ""
            }
        }
    },
    validations() {
        return {
            form: {
                firstName: { 
                    required
                },
                lastName: {
                    required
                },
                username: {
                    required
                },
                email: { 
                    required,
                    email
                },
                password: { 
                    password: {
                        required,
                        minLength: minLength(8)
                    },
                    confirmed: {
                        required,
                        sameAsPassword: sameAs(this.form.password.password)
                    }
                },
                gender: {
                    required
                }
            }
        }
    },
    methods: {
        createUser: async function() {

            this.v$.$validate()
            if (this.v$.$error) return

            await axios.post("http://127.0.0.1:5000/api/v1/register", this.form)
            .then(response => {

                var duplicate = response.data.duplicate

                if (duplicate) {
                    var element = document.getElementById(duplicate + "-exists")
                    element.style.display = "inline"
                    setTimeout(() => {
                        element.style.display = "none"
                    }, 5000)
                }
            })
            .catch(error => {
                console.log("New registration error: ", error);
            })
        }
    }    
}
</script>

<style scoped>

#email-exists {
    display: none;
}

#username-exists {
    display: none;
}

</style>
