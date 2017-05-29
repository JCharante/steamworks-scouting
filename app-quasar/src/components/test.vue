<template>
    <div class="list">
        <q-list-item
            :item="{
            label: 'Popover Not Opening',
            secondIcon: 'more_vert'
        }"
            link
        >
            <q-popover ref="firstPopover">
                <div class="list">
                    <div class="item item-link" @click="$refs.firstPopover.close()">
                        <div class="item-content">Edit</div>
                    </div>
                    <div class="item item-link" @click="$refs.firstPopover.close()">
                        <div class="item-content">Delete</div>
                    </div>
                </div>
            </q-popover>
        </q-list-item>

        <hr>

        <div>
            <q-list-item
                :item="{
                label: 'Popover Not Aligned Correctly',
                secondIcon: 'more_vert'
            }"
                link
            ></q-list-item>
            <q-popover ref="secondPopover">
                <div class="list">
                    <div class="item item-link" @click="$refs.secondPopover.close()">
                        <div class="item-content">Edit</div>
                    </div>
                    <div class="item item-link" @click="$refs.secondPopover.close()">
                        <div class="item-content">Delete</div>
                    </div>
                </div>
            </q-popover>
        </div>

        <hr>

        <div class="item">
            <div class="item-content has-secondary">
                <div>Not Using q-list-item</div>
            </div>
            <div class="item-secondary">
                <i slot="target">
                    more_vert
                    <q-popover ref="thirdPopover">
                        <div class="list">
                            <div class="item item-link" @click="$refs.thirdPopover.close()">
                                <div class="item-content">Edit</div>
                            </div>
                            <div class="item item-link" @click="$refs.thirdPopover.close()">
                                <div class="item-content">Delete</div>
                            </div>
                        </div>
                    </q-popover>
                </i>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {}
        }
    }
</script>
