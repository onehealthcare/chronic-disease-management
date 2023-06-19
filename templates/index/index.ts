NewApp({
    data() {
        return {
            message: ''
        }
    },
    methods: {
        greeting() {
            this.message = 'Hello World'
        },
        change() {
            this.message = this.message + 1
        }
    },
    mounted() {
        this.greeting()
    }
}).mount('#app')
