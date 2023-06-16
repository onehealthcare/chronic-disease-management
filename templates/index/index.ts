NewApp({
    data() {
        return {
            message: ''
        }
    },
    methods: {
        greeting() {
            this.message = 'Hello Vue.js!'
        },
        change() {
            this.message = this.message + 1
        }
    },
    mounted() {
        this.greeting()
    }
}).mount('#app')
