<template>
    <div v-if="displayAlerts" :class="[(status=='success' || status=='error')? (( status!=='success' ) ? alertDanger : alertSuccess) : 'alert']">
        <ul v-if="status=='error'">
            <li v-for="error in errors">{{ error }}</li>
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

    const alertSuccess = " alert alert-success";
    const alertDanger = " alert alert-danger";
    let displayAlerts=ref(false);

    let status=ref("");
    let errors = ref([]);
    let message = ref("");

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

    function clearAlerts() {
        displayAlerts.value = false;
    }
    
    function saveMovie() {
        
        let form_data = new FormData($('#movieForm')[0]);
        clearAlerts();

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
            const res = response.json();
            if (response.status===400) {
                return res;
            }
            return res;
        })
        .then(function (data) {
            // display a success message
            status = data.status;
            displayAlerts.value = true;
            console.log("STATUS:", status);
            if (status == "error") {
                errors.value = data.errors;
                console.log(errors.value);
            } else {
                errors.value = []
                message.value = data.message;
            }
            console.log(data);
        })
    }

</script>

<style></style>