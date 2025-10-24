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

    function getDifficultyColor(level) {
        const colors = {
            1: 'from-emerald-400 to-emerald-600',
            2: 'from-blue-400 to-blue-600', 
            3: 'from-amber-400 to-amber-600',
            4: 'from-orange-400 to-orange-600',
            5: 'from-rose-400 to-rose-600'
        };
        return colors[level] || 'from-gray-400 to-gray-600';
    }

    function formatExample(example) {
        // Check if the example contains the expected format with parentheses and dashes
        if (!example) return null;
        
        const parts = {
            chinese: '',
            pinyin: '',
            english: ''
        };
        
        // Try to parse the format: "Chinese (Pinyin) - English translation"
        const match = example.match(/^(.+?)\s*\((.+?)\)\s*-\s*(.+)$/);
        
        if (match) {
            parts.chinese = match[1].trim();
            parts.pinyin = match[2].trim();
            parts.english = match[3].trim();
        } else {
            // If format doesn't match, just show the raw text
            parts.chinese = example;
        }
        
        return parts;
    }

    $: filteredRules = selectedLanguage ? 
        rules.filter(rule => rule.language_id === selectedLanguage) : 
        rules;
</script>

<svelte:head>
    <title>Grammar Rules - Zayas Grammar</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8">
    <div class="container mx-auto px-4">
        <!-- Header -->
        <div class="text-center mb-12">
            <div class="inline-block bg-gradient-to-r from-slate-800 to-slate-600 text-transparent bg-clip-text">
                <h1 class="text-5xl font-bold mb-4">Grammar Rules Database</h1>
            </div>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
                Discover elegant grammar rules across multiple languages with detailed explanations and curated examples.
            </p>
        </div>

        <!-- Language Filter -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-8 mb-12 border border-white/20">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                <div class="flex-1">
                    <h2 class="text-2xl font-semibold text-slate-800 mb-3">Filter by Language</h2>
                    <p class="text-slate-600 text-base">Select a language to explore its unique grammatical structure</p>
                </div>
                <div class="flex flex-col sm:flex-row gap-4">
                    <select 
                        bind:value={selectedLanguage}
                        class="border border-slate-300 rounded-xl px-5 py-3 min-w-52 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:border-transparent bg-white/50 backdrop-blur-sm text-slate-700 font-medium transition-all duration-200 hover:border-slate-400"
                    >
                        <option value="">All Languages ({rules.length} rules)</option>
                        {#each languages as lang}
                            <option value={lang.language_id}>
                                {lang.language_name} ({lang.rule_count || 0})
                            </option>
                        {/each}
                    </select>
                    <button 
                        on:click={() => loadGrammarRules(selectedLanguage)}
                        class="bg-gradient-to-r from-slate-700 to-slate-600 text-white px-8 py-3 rounded-xl hover:from-slate-800 hover:to-slate-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 shadow-lg font-semibold"
                    >
                        Apply Filter
                    </button>
                </div>
            </div>
        </div>

        <!-- Language Quick Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {#each languages as lang}
                <div 
                    class="group bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-lg cursor-pointer hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
                    on:click={() => { selectedLanguage = lang.language_id; loadGrammarRules(lang.language_id); }}
                >
                    <div class="flex items-center justify-between mb-3">
                        <span class="font-bold text-slate-800 text-lg group-hover:text-slate-900 transition-colors">
                            {lang.language_name}
                        </span>
                        <span class="bg-gradient-to-r from-slate-600 to-slate-500 text-white text-xs px-3 py-1.5 rounded-full font-semibold shadow-sm">
                            {lang.language_id}
                        </span>
                    </div>
                    <div class="text-sm text-slate-500 mb-2">{lang.language_family}</div>
                    <div class="text-xs text-slate-400 font-medium">
                        {lang.rule_count || 0} rules available
                    </div>
                </div>
            {/each}
        </div>

        <!-- Rules Display -->
        {#if loading}
            <div class="text-center py-16">
                <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-slate-600 mx-auto mb-4"></div>
                <p class="text-slate-600 text-lg font-medium">Loading grammar rules...</p>
            </div>
        {:else if error}
            <div class="bg-red-50/80 backdrop-blur-sm border border-red-200 rounded-2xl p-8 text-center shadow-lg">
                <div class="text-red-500 text-4xl mb-4">⚠️</div>
                <p class="text-red-800 font-semibold text-lg mb-2">Error Loading Rules</p>
                <p class="text-red-600 mb-6">{error}</p>
                <button 
                    on:click={() => loadGrammarRules(selectedLanguage)}
                    class="bg-gradient-to-r from-red-600 to-red-500 text-white px-6 py-3 rounded-xl hover:from-red-700 hover:to-red-600 transition-all duration-200 transform hover:scale-105 shadow-lg font-semibold"
                >
                    Try Again
                </button>
            </div>
        {:else if filteredRules.length === 0}
            <div class="bg-amber-50/80 backdrop-blur-sm border border-amber-200 rounded-2xl p-12 text-center shadow-lg">
                <div class="text-amber-500 text-5xl mb-6">📚</div>
                <p class="text-amber-800 font-semibold text-xl mb-3">No Grammar Rules Found</p>
                <p class="text-amber-600 text-lg">Try selecting a different language or check back later for updates.</p>
            </div>
        {:else}
            <div class="grid gap-8">
                {#each filteredRules as rule (rule.rule_id)}
                    <div class="group bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden">
                        <!-- Header with Gradient -->
                        <div class="bg-gradient-to-r {getDifficultyColor(rule.difficulty_level)} p-6">
                            <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                                <div class="flex-1">
                                    <div class="flex items-center gap-4 mb-3">
                                        <h3 class="text-2xl font-bold text-white">{rule.rule_name}</h3>
                                        <span class="bg-white/20 text-white text-sm px-4 py-1.5 rounded-full font-semibold backdrop-blur-sm border border-white/30">
                                            {rule.language.language_name}
                                        </span>
                                    </div>
                                    <p class="text-white/90 leading-relaxed text-lg font-light">{rule.rule_description}</p>
                                </div>
                                <div class="flex flex-col items-end gap-3">
                                    <div class="text-white font-semibold text-sm bg-black/20 px-4 py-2 rounded-xl backdrop-blur-sm border border-white/20">
                                        Difficulty: <span class="text-yellow-300 ml-1">{getDifficultyStars(rule.difficulty_level)}</span>
                                    </div>
                                    <div class="text-white/80 text-xs font-medium">
                                        Level {rule.difficulty_level}/5
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Content Area -->
                        <div class="p-6">
                            <!-- Examples Section -->
                            {#if rule.examples && rule.examples.length > 0}
                                <div class="mb-6">
                                    <h4 class="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
                                        <span class="bg-slate-100 p-2 rounded-lg">💡</span>
                                        Examples
                                    </h4>
                                    <ul class="space-y-4">
                                        {#each rule.examples as example}
                                            {#const formattedExample = formatExample(example.example_sentence)}
                                            <li class="bg-slate-50/80 rounded-xl border border-slate-200/60 p-4 shadow-sm hover:shadow-md transition-shadow duration-200">
                                                {#if formattedExample && formattedExample.pinyin}
                                                    <!-- Formatted example with separate lines -->
                                                    <div class="space-y-2">
                                                        <div class="text-xl font-medium text-slate-800 leading-relaxed">
                                                            {formattedExample.chinese}
                                                        </div>
                                                        <div class="text-slate-600 font-normal italic leading-relaxed">
                                                            {formattedExample.pinyin}
                                                        </div>
                                                        <div class="text-slate-700 font-light leading-relaxed border-t border-slate-200/40 pt-2">
                                                            {formattedExample.english}
                                                        </div>
                                                    </div>
                                                {:else}
                                                    <!-- Fallback for unformatted examples -->
                                                    <div class="text-slate-700 leading-relaxed">
                                                        {example.example_sentence}
                                                    </div>
                                                {/if}
                                            </li>
                                        {/each}
                                    </ul>
                                </div>
                            {/if}
                            
                            <!-- Additional Info -->
                            <div class="flex flex-wrap items-center gap-4 text-sm text-slate-500 border-t border-slate-200/60 pt-4 mt-4">
                                <span class="flex items-center gap-2">
                                    <span class="bg-slate-100 p-1.5 rounded-lg">🌐</span>
                                    Language Code: <span class="font-mono bg-slate-100 px-3 py-1 rounded-lg text-slate-700 font-semibold">{rule.language_id}</span>
                                </span>
                                <span class="flex items-center gap-2">
                                    <span class="bg-slate-100 p-1.5 rounded-lg">🏛️</span>
                                    Family: {rule.language.language_family}
                                </span>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}

        <!-- Footer -->
        <div class="text-center mt-16 text-slate-500 text-base">
            <p class="font-medium">Zayas Grammar Database • {rules.length} grammar rules across {languages.length} languages</p>
            <p class="text-sm mt-2 text-slate-400">Elegantly designed for linguistic exploration</p>
        </div>
    </div>
</div>

<style>
    .container {
        max-width: 1200px;
    }
    
    /* Custom scrollbar for select */
    select {
        scrollbar-width: thin;
        scrollbar-color: #cbd5e1 #f1f5f9;
    }
    
    select::-webkit-scrollbar {
        width: 6px;
    }
    
    select::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }
    
    select::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    select::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>