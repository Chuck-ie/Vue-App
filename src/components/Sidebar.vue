<template>
	<button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
		Sidebar
	</button>
	<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
		<div class="offcanvas-header">
			<h5 class="offcanvas-title" id="offcanvasExampleLabel">Chuckie-Droid</h5>
			<button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
		</div>
		<div class="offcanvas-body">
			<nav class="navbar navbar-light bg-light">
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/">Home</router-link>
					<fas icon="home"/>
				</div>
			</nav>
			<nav class="navbar navbar-light bg-light">
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/login">Login</router-link>
					<fas icon="sign-in-alt"/>
				</div>
			</nav>
			<nav class="navbar navbar-light bg-light">
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/registration">Registration</router-link>
					<fas icon="sign-in-alt"/>
				</div>
			</nav>
			<nav class="navbar navbar-light bg-light">
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/calculator">Calculator</router-link>
					<fas icon="calculator"/>
				</div>
			</nav>
		</div>
	</div>
</template>
