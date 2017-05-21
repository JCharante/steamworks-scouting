<template>
    <!-- in each page -->
    <div> <!-- root node required for subRoutes -->
        <div class="layout-padding">
            ...page content...
        </div>
        <!--
          You can have as many <div>s with
          "layout-padding" CSS class as you want
        -->
        <!--
          Also, anything placed outside of these <div>s with "layout-padding"
          (so direct children of the root node) will have width 100% of your
          page view
        -->
    </div>
</template>
