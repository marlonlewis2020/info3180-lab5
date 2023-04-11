<template>
    <div :class="[status ? alertSuccessClass : alertErrorClass]" class="alert">
        <ul v-if="status=='error'">
            <li v-for="error in errors.value">{{ error }}</li>
        </ul>
        <span v-else>{{ message }}</span>
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

    const alertSuccess = "alert-success";
    const alertDanger = "alert-danger";
    let status=ref(false);
    let errors = ref([]);
    let message;
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
            if (status == "error") {
                errors = data.errors;
            } else {
                message = data.message;
            }
            console.log(data);
        })
        .catch(function(error) {
            console.log(error);
        });
    }

</script>

<style></style>