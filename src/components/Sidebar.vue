<template>
	<div class="dummySidebar position-fixed fs-3" data-bs-toggle="offcanvas" data-bs-target="#sidebar" aria-controls="sidebar">
		<fas icon="bars"/>
	</div>
	<div class="offcanvas offcanvas-start" tabindex="-1" id="sidebar" aria-labelledby="sidebarHeader">
		<div class="offcanvas-header">
			<h5 class="offcanvas-title" id="sidebarHeader">Chuckie-Droid</h5>
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
					<router-link class="navbar-brand" to="/projects">Projects</router-link>
					<fas icon="code-branch"/>
				</div>
			</nav>	
			<nav class="navbar navbar-light bg-light">
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/login">Login</router-link>
					<fas icon="sign-in-alt"/>
				</div>
			</nav>	
		</div>
	</div>
</template>

<style scoped>

.dummySidebar {
	min-height: 100%;
	width: 3rem;
	padding-right: 0.8rem;
	background-color: #198754;
	text-align: right;
}

</style>