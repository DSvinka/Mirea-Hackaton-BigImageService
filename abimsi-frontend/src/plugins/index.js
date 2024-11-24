import vuetify from './vuetify'

import pinia from './pinia'
import notify from './notify'

import router from '@/router'

import { DataLoaderPlugin} from 'unplugin-vue-router/data-loaders'

export function registerPlugins (app) {
  app
    .use(vuetify)

    .use(pinia)
    .use(notify)

    .use(DataLoaderPlugin, {router})
    .use(router)
}
