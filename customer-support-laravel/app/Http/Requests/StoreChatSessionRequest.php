<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Support\Facades\Config;
use Illuminate\Validation\Rule;

class StoreChatSessionRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        // Allow any authenticated user to create a chat session for themselves
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        // Get the valid keys from the AI configuration file
        $validConfigKeys = array_keys(Config::get('ai_configurations', []));

        return [
            'ai_configuration_key' => [
                'nullable', // Allow it to be missing (will use default)
                'string',
                Rule::in($validConfigKeys), // Must be one of the keys defined in the config
            ],
            // Add other rules if needed for other fields
        ];
    }
}
