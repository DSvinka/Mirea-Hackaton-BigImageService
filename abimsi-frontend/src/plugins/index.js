import vuetify from './vuetify'

import pinia from './pinia'
import notify from './notify'

import router from '@/router'

export function registerPlugins (app) {
  app
    .use(vuetify)

    .use(pinia)
    .use(notify)

    .use(router)
}
