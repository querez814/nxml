import type { PageLoad } from './$types';
import { marked } from 'marked';
import siteMetadata from '$lib/config/site-metadata';
import { redirect } from '@sveltejs/kit';

function validateMarkdownPath(filePath: string) {
    const regex = /^\.\.\/([a-zA-Z0-9_-]+)\.md$/;
    return regex.test(filePath);
}

function extractFilename(filePath: string): string | null {
    const regex = /^\.\.\/([a-zA-Z0-9_-]+)\.md$/;
    const match = filePath.match(regex);
    return match ? match[1] : null; // Return the captured group if a match is found
}

// Define the type for the module structure if necessary
interface MarkdownModule {
    default: string;
}

  
export const load = (async ({ params }) => {
    const legalDocuments: Record<string, string> = import.meta.glob('../*.md', {   
        query: '?raw', 
        import: 'default',
        eager: true
    });

    for (const path in legalDocuments) {
        if (validateMarkdownPath(path)) {
            const filename = extractFilename(path);
          
            if(filename === params.slug) {
                // Will be sanitized on the frontend
                return { html:  await marked(legalDocuments[path]), };
            }
        }
    }

    redirect(303, siteMetadata.urls.web.notFound);
}) satisfies PageLoad;
