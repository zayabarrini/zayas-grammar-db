<script>
    import { onMount } from 'svelte';
    
    let languages = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        try {
            const response = await fetch('http://localhost:8000/languages/');
            if (!response.ok) throw new Error('Failed to fetch languages');
            languages = await response.json();
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    });
</script>

<svelte:head>
    <title>Languages - Zayas Grammar</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Languages</h1>
    
    {#if loading}
        <div class="text-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-4 text-gray-600">Loading languages...</p>
        </div>
    {:else if error}
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800">Error: {error}</p>
        </div>
    {:else}
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each languages as language}
                <div class="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
                    <h2 class="text-xl font-semibold text-gray-800 mb-2">
                        {language.language_name}
                    </h2>
                    <p class="text-gray-600 text-sm mb-2">
                        Code: <span class="font-mono bg-gray-100 px-2 py-1 rounded">{language.language_id}</span>
                    </p>
                    <p class="text-gray-600 text-sm">
                        Family: {language.language_family}
                    </p>
                    <p class="text-gray-600 text-sm">
                        Script: {language.script}
                    </p>
                </div>
            {/each}
        </div>
    {/if}
    
    <div class="mt-8">
        <a href="/" class="text-blue-600 hover:text-blue-800">← Back to Home</a>
    </div>
</div>