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
            const response = await fetch('http://localhost:8000/languages/with-rules/count');
            languages = await response.json();
        } catch (err) {
            console.error('Failed to load languages:', err);
            // Fallback to basic languages endpoint
            try {
                const response = await fetch('http://localhost:8000/languages/');
                const basicLanguages = await response.json();
                languages = basicLanguages.map(lang => ({ ...lang, rule_count: 0 }));
            } catch (fallbackErr) {
                console.error('Failed to load basic languages:', fallbackErr);
            }
        }
    }
    async function loadGrammarRules(lang = '') {
        loading = true;
        try {
            const url = lang ? `http://localhost:8000/grammar/rules/${lang}` : 'http://localhost:8000/grammar/rules';
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch rules');
            const data = await response.json();
            
            // Pre-process examples for all rules
            rules = data.map(rule => ({
                ...rule,
                formattedExamples: rule.examples ? rule.examples.map(example => 
                    formatExample(example.example_sentence)
                ) : []
            }));
            
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
        if (!example) return { chinese: '', pinyin: '', english: '', raw: example };
        
        // Try to parse the format: "Chinese (Pinyin) - English translation"
        const match = example.match(/^(.+?)\s*\((.+?)\)\s*-\s*(.+)$/);
        
        if (match) {
            return {
                chinese: match[1].trim(),
                pinyin: match[2].trim(),
                english: match[3].trim(),
                raw: example,
                isFormatted: true
            };
        } else {
            // If format doesn't match, return raw text
            return {
                chinese: example,
                pinyin: '',
                english: '',
                raw: example,
                isFormatted: false
            };
        }
    }

    $: filteredRules = selectedLanguage ? 
        rules.filter(rule => rule.language_id === selectedLanguage) : 
        rules;
</script>

<svelte:head>
    <title>Grammar Rules - Zayas Grammar</title>
</svelte:head>

<div class="grammar-page-bg">
    <div class="container">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-4xl font-bold mb-4">Grammar Rules Database</h1>
            <p class="text-lg max-w-2xl mx-auto">
                Explore grammar rules across multiple languages with detailed explanations and examples.
            </p>
        </div>

        <!-- Language Filter -->
        <div class="filter-section">
            <div class="filter-content">
                <h2>Filter by Language</h2>
                <p>Select a language to view its specific grammar rules</p>
                <div class="filter-controls">
                    <select bind:value={selectedLanguage} class="custom-scrollbar">
                        <option value="">All Languages ({rules.length} rules)</option>
                        {#each languages as lang}
                            <option value={lang.language_id}>
                                {lang.language_name} ({lang.rule_count || 0})
                            </option>
                        {/each}
                    </select>
                    <button on:click={() => loadGrammarRules(selectedLanguage)}>
                        Apply Filter
                    </button>
                </div>
            </div>
        </div>

        <!-- Language Quick Stats -->
        <div class="language-stats-grid">
            {#each languages as lang}
                <div 
                    class="language-stat-card"
                    on:click={() => { selectedLanguage = lang.language_id; loadGrammarRules(lang.language_id); }}
                >
                    <div class="stat-header">
                        <span class="language-name">{lang.language_name}</span>
                        <span class="language-code">{lang.language_id}</span>
                    </div>
                    <div class="language-family">{lang.language_family}</div>
                    <div class="rule-count">{lang.rule_count || 0} rules available</div>
                </div>
            {/each}
        </div>

        <!-- Rules Display -->
        {#if loading}
            <div class="text-center py-16">
                <div class="loading-spinner"></div>
                <p>Loading grammar rules...</p>
            </div>
        {:else if error}
            <div class="error-state">
                <p>Error: {error}</p>
                <button on:click={() => loadGrammarRules(selectedLanguage)}>
                    Try Again
                </button>
            </div>
        {:else if filteredRules.length === 0}
            <div class="empty-state">
                <p>No grammar rules found.</p>
                <p>Try selecting a different language or check back later.</p>
            </div>
        {:else}
            <div class="rules-grid">
                {#each filteredRules as rule (rule.rule_id)}
                    <div class="grammar-card">
                        <!-- Header with Gradient -->
                        <div class="grammar-card-header">
                            <div class="card-header-content">
                                <div class="card-title-section">
                                    <div class="title-row">
                                        <h3>{rule.rule_name}</h3>
                                        <!-- <span class="language-badge">
                                            {rule.language.language_name}
                                        </span> -->
                                    </div>
                                    <p>{rule.rule_description}</p>
                                </div>
                                <!-- <div class="difficulty-section">
                                    <div class="difficulty-badge">
                                        Difficulty: <span class="stars">{getDifficultyStars(rule.difficulty_level)}</span>
                                    </div>
                                    <div class="level-text">
                                        Level {rule.difficulty_level}/5
                                    </div>
                                </div> -->
                            </div>
                        </div>
                        
                        <!-- Content Area -->
                        <div class="grammar-card-content">
                            <!-- Examples Section -->
                            {#if rule.formattedExamples && rule.formattedExamples.length > 0}
                                <div class="examples-section">
                                    <h4>Examples</h4>
                                    <ul class="examples-list">
                                        {#each rule.formattedExamples as formattedExample}
                                            <li class="grammar-example">
                                                {#if formattedExample.isFormatted}
                                                    <div class="example-content">
                                                        <div class="chinese-text">
                                                            {formattedExample.chinese}
                                                        </div>
                                                        <div class="pinyin-text">
                                                            {formattedExample.pinyin}
                                                        </div>
                                                        <div class="english-text">
                                                            {formattedExample.english}
                                                        </div>
                                                    </div>
                                                {:else}
                                                    <div class="raw-example">
                                                        {formattedExample.raw}
                                                    </div>
                                                {/if}
                                            </li>
                                        {/each}
                                    </ul>
                                </div>
                            {/if}
                            
                            <!-- Additional Info -->
                            <!-- <div class="additional-info">
                                <span>Language Code: <code>{rule.language_id}</code></span>
                                <span>Family: {rule.language.language_family}</span>
                            </div> -->
                        </div>
                    </div>
                {/each}
            </div>
        {/if}

        <!-- Footer -->
        <div class="footer">
            <p>Zayas Grammar Database • {rules.length} grammar rules across {languages.length} languages</p>
        </div>
    </div>
</div>