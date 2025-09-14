from infrastructure.fs_repo import compute_repo_metrics

class ScanRepoUseCase:
    def execute(self, root: str):
        return {"metrics": compute_repo_metrics(root)}
