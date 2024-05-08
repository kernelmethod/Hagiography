import adapter from '@sveltejs/adapter-static';

export default {
    kit: {
        adapter: adapter({
            // default options are shown. On some platforms
            // these options are set automatically — see below
            pages: 'build',
            assets: 'build',
            fallback: undefined,
            precompress: false,
            strict: true
        }),
        alias: {
            '$js': './src/js',
            '$components': './src/components',
        },
        prerender: {
            handleHttpError: ({path, referrer, message}) => {
                throw new Error(message);
            }
        },
        csp: {
            directives: {
                'default-src': ['self'],
                'style-src': ['self', 'unsafe-inline'],
            },
        }
    }
};
