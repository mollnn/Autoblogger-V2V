<template>
  <div class="sidebar-wrapper">
    <nav
      :class="{ sidebar: true, sidebarStatic, sidebarOpened }"
      @mouseenter="sidebarMouseEnter"
      @mouseleave="sidebarMouseLeave"
    >
      <header class="logo">
        <router-link to="/app/dashboard"
          ><span class="primary-word">V2V</span>
          <span class="secondary-word"> 视频管理后台</span></router-link
        >
      </header>
      <h5 class="navTitle first">V2V</h5>
      <ul class="nav">
        <NavLink
          :activeItem="activeItem"
          header="热点总览"
          link="/app/dashboard"
          iconName="flaticon-home"
          index="dashboard"
          isHeader
        />
        <!-- <NavLink
            :activeItem="activeItem"
            header="Components"
            link="/app/components"
            iconName="flaticon-network"
            index="components"
            :childrenLinks="[
              { header: 'Charts', link: '/app/components/charts' },
              { header: 'Icons', link: '/app/components/icons' },
              { header: 'Maps', link: '/app/components/maps' },
            ]"
        /> -->
        <NavLink
          :activeItem="activeItem"
          header="视频信息"
          link="/app/components/charts"
          iconName="flaticon-network"
          index="components"
          isHeader
        />
        <NavLink
          :activeItem="activeItem"
          header="管线管理"
          link="/app/typography"
          iconName="flaticon-list"
          index="typography"
          isHeader
        />
        <NavLink
          :activeItem="activeItem"
          header="管线状态"
          link="/app/tables"
          iconName="flaticon-equal-1"
          index="tables"
          isHeader
        />
        <NavLink
          :activeItem="activeItem"
          header="剪辑成片"
          link="/app/notifications"
          iconName="flaticon-bell"
          index="notifications"
          isHeader
        />
      </ul>
      <h5 class="navTitle">LINKS:</h5>
      <ul class="sidebarLabels">
        <li>
          <a href="http://47.242.173.26/#/page1" target="_blank">
            <i class="fa fa-circle text-danger" />
            <span class="labelName"> 精粹欣赏 </span>
          </a>
        </li>
        <li>
          <a href="https://www.bilibili.com/" target="_blank">
            <i class="fa fa-circle text-primary" />
            <span class="labelName"> 账号监控 </span>
          </a>
        </li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ul>
      <h5 class="navTitle"></h5>
    </nav>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import isScreen from "@/core/screenHelper";
import NavLink from "./NavLink/NavLink";

export default {
  name: "Sidebar",
  components: { NavLink },
  data() {
    return {
      alerts: [
        {
          id: 0,
          title: "Sales Report",
          value: 15,
          footer: "Calculating x-axis bias... 65%",
          color: "danger",
        },
        {
          id: 1,
          title: "Personal Responsibility",
          value: 20,
          footer: "Provide required notes",
          color: "primary",
        },
      ],
    };
  },
  methods: {
    ...mapActions("layout", ["changeSidebarActive", "switchSidebar"]),
    setActiveByRoute() {
      const paths = this.$route.fullPath.split("/");
      paths.pop();
      this.changeSidebarActive(paths.join("/"));
    },
    sidebarMouseEnter() {
      if (!this.sidebarStatic && (isScreen("lg") || isScreen("xl"))) {
        this.switchSidebar(false);
        this.setActiveByRoute();
      }
    },
    sidebarMouseLeave() {
      if (!this.sidebarStatic && (isScreen("lg") || isScreen("xl"))) {
        this.switchSidebar(true);
        this.changeSidebarActive(null);
      }
    },
  },
  created() {
    this.setActiveByRoute();
  },
  computed: {
    ...mapState("layout", {
      sidebarStatic: (state) => state.sidebarStatic,
      sidebarOpened: (state) => !state.sidebarClose,
      activeItem: (state) => state.sidebarActiveElement,
    }),
  },
};
</script>

<!-- Sidebar styles should be scoped -->
<style src="./Sidebar.scss" lang="scss" scoped/>
