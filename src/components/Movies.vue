<script setup>
    import { ref, onMounted } from "vue";

    let movies = ref([]);

    function fetchMovies(filename) {
        fetch('/api/v1/movies')
        .then((response) => response.json())
        .then((data) => { 
            console.log(data);
            movies.value = data.movies; });
    }

    onMounted(()=>{
        fetchMovies();
    });

</script>

<template>
    <h1>Movies</h1>
    
    <div class="flex-row">
        <div v-for="movie in movies" :key="movie.id" class="card flex-row" style="width:50%;height:250px;">
            <img class="card-img" :src="`uploads/${movie.poster}`" alt="movie image" style="width:30%;">
            <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
            </div>
        </div>
    </div>

</template>

