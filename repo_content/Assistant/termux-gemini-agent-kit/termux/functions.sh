#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Termux Gemini Agent Kit - Functions

gmode() {
    local cmd="${1:-}"
    local arg1="${2:-}"
    local arg2="${3:-}"

    case "$cmd" in
        google)
            unset GOOGLE_GENAI_USE_VERTEXAI
            unset GOOGLE_CLOUD_PROJECT
            unset GOOGLE_CLOUD_LOCATION
            echo "Switched to Google mode (default)."
            ;;
        vertex)
            if [ -z "$arg1" ]; then
                echo "Usage: gmode vertex <PROJECT_ID> [LOCATION]"
                echo "Default location: us-central1"
                return 1
            fi

            export GOOGLE_GENAI_USE_VERTEXAI="true"
            export GOOGLE_CLOUD_PROJECT="$arg1"

            # Use provided location, existing env var, or default to us-central1
            if [ -n "$arg2" ]; then
                export GOOGLE_CLOUD_LOCATION="$arg2"
            elif [ -z "${GOOGLE_CLOUD_LOCATION:-}" ]; then
                export GOOGLE_CLOUD_LOCATION="us-central1"
            fi

            echo "Switched to Vertex AI mode:"
            echo "  Project: $GOOGLE_CLOUD_PROJECT"
            echo "  Location: $GOOGLE_CLOUD_LOCATION"
            echo "Note: This change is temporary for this session."
            ;;
        status)
            echo "Current Mode:"
            if [ "${GOOGLE_GENAI_USE_VERTEXAI:-}" == "true" ]; then
                echo "  Mode: Vertex AI"
                echo "  Project: ${GOOGLE_CLOUD_PROJECT:-<unset>}"
                echo "  Location: ${GOOGLE_CLOUD_LOCATION:-<unset>}"
            else
                echo "  Mode: Google (Default)"
            fi
            ;;
        *)
            echo "Usage: gmode {google|vertex <PROJECT_ID> [LOCATION]|status}"
            return 1
            ;;
    esac
}
