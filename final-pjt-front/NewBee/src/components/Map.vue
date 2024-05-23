<template>
  <KakaoMap :lat="curLat" :lng="curLng" :width="'60rem'" :height="'40rem'"  class="mb-4" @onLoadKakaoMap="onLoadKakaoMap">
    <KakaoMapMarker :lat="curLat" :lng="curLng">
      <template v-slot:infoWindow>
        <div style="padding: 10px">현재 위치</div>
      </template>
    </KakaoMapMarker>
    <KakaoMapMarker v-for="(marker, index) in markerList" :key="marker.key === undefined ? index : marker.key"
      :lat="marker.lat" :lng="marker.lng" :infoWindow="marker.infoWindow" :clickable="true"
      @onClickKakaoMapMarker="onClickMapMarker(marker)" />
  </KakaoMap>
  <button class="btn btn-primary fw-bold" @click="getCurrentPos">현재 위치</button>
</template>

<script setup>
import { computed, ref } from 'vue'
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps'

// 라이브러리 사용 방법을 반드시 참고하여 주시기 바랍니다.
const map = ref();
const markerList = ref([])
const curLat = ref(37.501274)
const curLng = ref(127.039585)

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef
  watchCenterChange()
}

// 지도 중심 이동시 근처 은행 검색 및 마커 표시
const watchCenterChange = () => {
  if (map.value) {
    map.value.addListener('dragend', () => {
      const center = map.value.getCenter()
      console.log(center.getLat(), center.getLng())
      curLat.value = center.getLat()
      curLng.value = center.getLng()
      console.log(curLat.value, curLng.value)

      // 근처 은행 재검색
      const ps = new kakao.maps.services.Places();
      ps.keywordSearch('근처 은행', placesSearchCB, {
        location: new kakao.maps.LatLng(curLat.value, curLng.value)
      });
    })
  } else { console.error('지도 객체가 초기화되지 않았습니다.')}}

// 현재 위치 근처 은행 검색
const getCurrentPos = function () {
  navigator.geolocation.getCurrentPosition(function (pos) {
    curLat.value = pos.coords.latitude;
    curLng.value = pos.coords.longitude;

    // 지도 중심 이동
    panTo(curLat.value, curLng.value);

    // 장소 검색
    const ps = new kakao.maps.services.Places();
    ps.keywordSearch('근처 은행', placesSearchCB, {
      location: new kakao.maps.LatLng(curLat.value, curLng.value)
    })
  })
}

const panTo = function (lat, lng) {
  if (map.value) {
    map.value.panTo(new kakao.maps.LatLng(lat, lng));
  }
}


// 키워드 검색 완료 시 호출되는 콜백함수입니다
const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기 위해
    // LatLngBounds 객체에 좌표를 추가합니다
    const bounds = new kakao.maps.LatLngBounds();
    markerList.value = []; // 기존 마커 리스트 초기화

    for (let marker of data) {
      const markerItem = {
        lat: marker.y,
        lng: marker.x,
        infoWindow: {
          content: marker.place_name,
          visible: false
        }
      };
      markerList.value.push(markerItem);
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.value?.setBounds(bounds);
  }
}

// 마커 클릭 시 인포윈도우의 visible 값을 반전시킵니다
const onClickMapMarker = (markerItem) => {
  markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
}
</script>

<style scoped></style>
