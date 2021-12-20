<template>
    <h3>Loginform: </h3>
    <br>
    <br>
    <br>
    <br>
    <form class="container" @submit.prevent="login" novalidate>
        <div class="row offset-md-4 needs-validation">
            <div class="col-md-6">
                <label for="inputLoginName" class="form-label">Username or Email</label>
                <input v-model="form.loginName" type="text" class="form-control" id="inputLoginName" placeholder="Username or Email"
                v-bind:class="{
                    'is-valid': !v$.form.loginName.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.loginName.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.loginName.$invalid">
                    Please enter your username or email!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-4">
            <div class="col-md-6">
                <label for="inputPassword" class="form-label">Password</label>
                <input v-model="form.password" type="password" class="form-control" id="inputPassword" placeholder="Password"
                v-bind:class="{
                    'is-valid': !v$.form.password.$invalid && v$.form.$dirty,
                    'is-invalid': v$.form.password.$invalid && v$.form.$dirty
                    }"
                >
                <div class="invalid-feedback" v-if="v$.form.password.required.$invalid">
                    Please enter your password!
                </div>
            </div>
        </div>
        <br>
        <div class="row offset-md-4">
            <div class="col-md-2">
                <button type="submit" class="btn btn-outline-success">Login</button>
            </div>
            <div class="col-md-4">
                <router-link class="btn btn-outline-success" to="/registration">Sign up</router-link>
            </div>
        </div>
    </form>
</template>

<script>
import axios from "axios"
import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"

export default {
    data() {
        return {
            v$: useVuelidate(),
            form: {
                loginName: "",
                password: ""
            }
        }
    },
    validations() {
        return {
            form: {
                loginName: {
                    required
                },
                password: {
                    required
                }
            }
        }
    },
    methods: {
        login: async function() {

            this.v$.$validate()
            if (this.v$.$error) return

            await axios.post("http://127.0.0.1:5000/api/v1/login", this.form)
                .then(response => {
                    var loginError = response.data.loginError
                    if (loginError) {
                        // handle loginError
                        console.log(loginError, "error")
                    } else {
                        console.log("logged In");
                    }


                })
                .catch(error => {
                console.log("New login error: ", error);
                })
        }
    }
}
</script>

<style scoped>


</style>
