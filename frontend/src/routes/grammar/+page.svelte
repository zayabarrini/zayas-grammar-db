<script>
    import { onMount } from 'svelte';
    
    let rules = [];
    let languages = [];
    let selectedLanguage = '';
    let loading = true;
    let error = null;

    onMount(async () => {
        await loadLanguages();
        await loadGrammarRules();
        loading = false;
    });

    async function loadLanguages() {
        try {
            const response = await fetch('http://localhost:8000/grammar/languages-with-rules');
            languages = await response.json();
        } catch (err) {
            console.error('Failed to load languages:', err);
        }
    }

    async function loadGrammarRules(lang = '') {
        loading = true;
        try {
            const url = lang ? `http://localhost:8000/grammar/rules/${lang}` : 'http://localhost:8000/grammar/rules';
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch rules');
            rules = await response.json();
            error = null;
        } catch (err) {
            error = err.message;
            rules = [];
        } finally {
            loading = false;
        }
    }

    function getDifficultyStars(level) {
        return '★'.repeat(level) + '☆'.repeat(5 - level);
    }

    $: filteredRules = selectedLanguage ? 
        rules.filter(rule => rule.language_id === selectedLanguage) : 
        rules;
</script>

<svelte:head>
    <title>Grammar Rules - Zayas Grammar</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-4">Grammar Rules Database</h1>
            <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                Explore grammar rules across 8 languages with detailed explanations and difficulty levels.
            </p>
        </div>

        <!-- Language Filter -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h2 class="text-xl font-semibold text-gray-800 mb-2">Filter by Language</h2>
                    <p class="text-gray-600 text-sm">Select a language to view its specific grammar rules</p>
                </div>
                <div class="flex gap-4">
                    <select 
                        bind:value={selectedLanguage}
                        class="border border-gray-300 rounded-lg px-4 py-2 min-w-48 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="">All Languages ({rules.length} rules)</option>
                        {#each languages as lang}
                            <option value={lang.language_id}>
                                {lang.language_name} 
                            </option>
                        {/each}
                    </select>
                    <button 
                        on:click={() => loadGrammarRules(selectedLanguage)}
                        class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Apply Filter
                    </button>
                </div>
            </div>
        </div>

        <!-- Language Quick Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {#each languages as lang}
                <div 
                    class="bg-white rounded-lg shadow-sm p-4 border border-gray-200 cursor-pointer hover:shadow-md transition-shadow"
                    on:click={() => { selectedLanguage = lang.language_id; loadGrammarRules(lang.language_id); }}
                >
                    <div class="flex items-center justify-between">
                        <span class="font-semibold text-gray-800">{lang.language_name}</span>
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                            {lang.language_id}
                        </span>
                    </div>
                    <div class="text-sm text-gray-500 mt-2">{lang.language_family}</div>
                </div>
            {/each}
        </div>

        <!-- Rules Display -->
        {#if loading}
            <div class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-gray-600">Loading grammar rules...</p>
            </div>
        {:else if error}
            <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <p class="text-red-800 font-medium">Error: {error}</p>
                <button 
                    on:click={() => loadGrammarRules(selectedLanguage)}
                    class="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                >
                    Try Again
                </button>
            </div>
        {:else if filteredRules.length === 0}
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
                <p class="text-yellow-800 text-lg">No grammar rules found.</p>
                <p class="text-yellow-600 mt-2">Try selecting a different language or check back later.</p>
            </div>
        {:else}
            <div class="grid gap-6">
                {#each filteredRules as rule}
                    <div class="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
                        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-4">
                            <div class="flex-1">
                                <div class="flex items-center gap-3 mb-2">
                                    <h3 class="text-xl font-semibold text-gray-800">{rule.rule_name}</h3>
                                    <span class="bg-gray-100 text-gray-800 text-sm px-3 py-1 rounded-full font-medium">
                                        {rule.language.language_name}
                                    </span>
                                </div>
                                <p class="text-gray-600 leading-relaxed">{rule.rule_description}</p>
                                
                                <!-- Examples Section -->
                                {#if rule.examples && rule.examples.length > 0}
                                    <div class="mt-4 border-t border-gray-100 pt-4">
                                    <h4 class="text-sm font-semibold text-gray-700 mb-2">Examples:</h4>
                                    <ul class="space-y-2 text-sm">
                                        {#each rule.examples as example}
                                        <li class="text-gray-600 bg-gray-50 px-3 py-2 rounded border border-gray-200">
                                            {example.example_sentence}
                                        </li>
                                        {/each}
                                    </ul>
                                    </div>
                                {/if}
                            </div>
                            <div class="flex flex-col items-end gap-2">
                                <div class="text-sm text-gray-500">
                                    Difficulty: <span class="font-medium text-yellow-600">{getDifficultyStars(rule.difficulty_level)}</span>
                                </div>
                                <div class="text-xs text-gray-400">
                                    Level {rule.difficulty_level}/5
                                </div>
                            </div>
                        </div>
                        
                        <!-- Additional info could go here -->
                        <div class="flex items-center gap-4 text-sm text-gray-500 border-t border-gray-100 pt-4 mt-4">
                            <span>Language Code: <span class="font-mono bg-gray-100 px-2 py-1 rounded">{rule.language_id}</span></span>
                            <span>Family: {rule.language.language_family}</span>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}

        <!-- Footer -->
        <div class="text-center mt-12 text-gray-500 text-sm">
            <p>Zayas Grammar Database • {rules.length} grammar rules across {languages.length} languages</p>
        </div>
    </div>
</div>

<style>
    .container {
        max-width: 1200px;
    }
</style>