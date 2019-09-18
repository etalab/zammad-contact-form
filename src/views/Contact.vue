<template>
  <div class="container">
    <h1>Contactez-nous</h1>
    <b-alert :show="error" variant="danger">Quelque chose s'est mal passé, désolé. Merci de réessayer. Vous pouvez aussi nous écrire à support@data.gouv.fr.</b-alert>
    <b-alert :show="success" variant="success">Votre message a bien été envoyé. Nous vous répondrons dès que possible. Votre numéro de ticket est le <strong>{{ ticketId }}</strong>.</b-alert>
    <b-form v-if="!success" @submit.prevent="onSubmit" method="POST">
      <b-form-group label="Votre nom" label-for="input-name">
        <b-form-input
          id="input-name"
          v-model="form.name"
          required
          placeholder="Jean-Michel Data"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        label="Votre adresse email"
        label-for="input-email"
        description="Pour que nous puissions vous répondre."
      >
        <b-form-input
          id="input-email"
          v-model="form.email"
          type="email"
          required
          placeholder="jean-michel@data.gouv.fr"
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Sujet de votre demande" label-for="input-subject"
        :description="currentCategory && currentCategory.description">
        <b-form-select
          id="input-subject"
          v-model="form.category"
          :options="categories"
          required
        >
          <template v-slot:first>
            <option :value="null" disabled>-- Choisissez un sujet --</option>
          </template>
        </b-form-select>
      </b-form-group>

      <b-form-group label="Titre de votre demande" label-for="input-title">
        <b-form-input
          id="input-title"
          v-model="form.title"
          required
          placeholder="Accès aux données de..."
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Détail de votre demande" label-for="input-message">
        <b-form-textarea
          id="input-message"
          v-model="form.message"
          placeholder="..."
          rows="10"
          required
        ></b-form-textarea>
      </b-form-group>

      <input id="last_name" type="text" name="last_name" v-model="form.last_name" />

      <b-button :disabled="sending" type="submit" variant="primary">
        <b-spinner small v-if="sending"></b-spinner> Envoyer
      </b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  name: 'home',
  components: {},
  data () {
    return {
      form: {
        email: '',
        category: this.$route.query.group,
        title: '',
        message: '',
        // honey pot
        last_name: ''
      },
      categories: [
        { value: 'support@data.gouv.fr', text: 'Support technique data.gouv.fr', description: "Support de la plateforme data.gouv.fr en tant qu'utilisateur ou producteur" },
        { value: 'ouverture@data.gouv.fr', text: "Demande d'ouverture de données", description: 'Données publiques difficiles à trouver ou inexistantes' },
        { value: 'test@data.gouv.fr', text: 'Groupe de test', description: 'Pour envoyer des tests' }
      ],
      sending: false,
      error: false,
      success: false,
      ticketId: ''
    }
  },
  computed: {
    currentCategory () {
      if (!this.form.category) return
      return this.categories.find(c => {
        return c.value === this.form.category
      })
    }
  },
  methods: {
    onSubmit () {
      this.sending = true
      this.$http.post('/api', this.form).then(res => {
        this.ticketId = res.body && res.body.id
        this.success = true
      }).catch(err => {
        this.error = true
        console.error(err)
      }).finally(() => {
        this.sending = false
      })
    }
  },
  watch: {
    'form.category': function (newVal) {
      this.$router.push({ query: { ...this.$route.query, group: newVal } })
    }
  }
}
</script>

<style scoped>
#last_name {
  display: none;
}
</style>
