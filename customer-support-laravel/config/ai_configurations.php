<?php

return [
    /*
    |--------------------------------------------------------------------------
    | AI Configurations for User Selection
    |--------------------------------------------------------------------------
    |
    | Define the different AI setups users can choose from.
    | Each key is a unique identifier stored in the database.
    | 'name' is the user-facing display name for the dropdown.
    | 'provider', 'model', 'system_prompt_view' define the AI settings.
    |
    */

    'default' => [
        'name' => 'Standard (Gemini Flash)',
        'provider' => env('AI_CONFIG_DEFAULT_PROVIDER', 'gemini'),
        'model' => env('AI_CONFIG_DEFAULT_MODEL', 'gemini-1.5-flash-latest'),
        'system_prompt_view' => env('AI_CONFIG_DEFAULT_PROMPT_VIEW', 'prompts.support-system-prompt'),
    ],

    'gemini-pro' => [
        'name' => 'Advanced (Gemini Pro)',
        'provider' => env('AI_CONFIG_GEMINI_PRO_PROVIDER', 'gemini'),
        'model' => env('AI_CONFIG_GEMINI_PRO_MODEL', 'gemini-1.5-pro-latest'),
        'system_prompt_view' => env('AI_CONFIG_GEMINI_PRO_PROMPT_VIEW', 'prompts.support-system-prompt'),
    ],

    'alternative-prompt' => [
        'name' => 'Experimental Prompt (Gemini Flash)',
        'provider' => env('AI_CONFIG_ALT_PROMPT_PROVIDER', 'gemini'),
        'model' => env('AI_CONFIG_ALT_PROMPT_MODEL', 'gemini-1.5-flash-latest'), // Same model, different prompt
        'system_prompt_view' => env('AI_CONFIG_ALT_PROMPT_PROMPT_VIEW', 'prompts.support-system-prompt-experimental'), // Needs view: prompts/support-system-prompt-experimental.blade.php
    ],

    // Add more configurations as needed, e.g., for different providers like Anthropic
    /*
    'claude-sonnet' => [
        'name' => 'Anthropic (Claude 3.5 Sonnet)',
        'provider' => 'anthropic', // Make sure 'anthropic' is configured in config/prism.php
        'model' => 'claude-3-5-sonnet-20240620',
        'system_prompt_view' => 'prompts.support-system-prompt',
    ],
    */

];