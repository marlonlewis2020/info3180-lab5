<template>
    <div :class="[response, bg-danger]" :value="status"  v-if="value">
        <ul v-if="value=='error'">
            <li v-for="error in errors">{{ error }}</li>
        </ul>
    </div>
    <div class="response" :value="status" v-if="value=='success'">
        <span class="alert alert-success">{{ message }}</span>
    </div>
    <form id="movieForm" action="" method="post" @submit.prevent="saveMovie">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" name="description" class="form-control" > </textarea>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster</label>
            <input type="file" id="poster" name="poster" class="form-control" />
        </div>
        <button type="submit" name="submit" id="submit" class="btn btn-primary d-flex justify-content-center"> Submit </button>
    </form>
</template>

<script setup>
    import { ref, onMounted } from "vue";

    let status;
    let message;
    let errors;

    let csrf_token = ref("");

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
    }

    onMounted(() => {
        getCsrfToken();
    });
    
    function saveMovie() {
        // const poster = $('#poster').files[0];
        // console.log("poster:", poster);
        let form_data = new FormData($('#movieForm')[0]);

        fetch("/api/v1/movies", {
            method: 'POST',
            headers: {
                // 'Accept': 'application/json',
                // 'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token.value
            },
            body: form_data
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // display a success message
            status = data.status;
            message = data.message;
            console.log(data);
        })
        .catch(function (error) {
            status = error.status;
            errors = error.errors;
            console.log(error);
        });
    }

</script>

<style></style>