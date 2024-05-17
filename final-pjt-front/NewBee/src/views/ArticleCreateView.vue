<template>
    <div>
        <h1 class="text-center">게시글 작성</h1>
        <div class="container">
            <form>
                <div class="mb-3">
                    <label for="title" class="form-label">제목</label>
                    <input type="text" class="form-control" id="title" placeholder="제목을 입력하세요">
                </div>
                <div class="mb-3">
                    <label for="content" class="form-label">내용</label>
                    <textarea class="form-control" id="content" rows="3" placeholder="내용을 입력하세요"></textarea>
                </div>
                <button type="submit" class="btn btn-warning">작성</button>
            </form>
        </div>
    </div>
</template>

<script setup>

</script>

<style scoped>
</style>