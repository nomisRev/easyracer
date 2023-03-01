import io.kotest.core.extensions.install
import io.kotest.core.spec.style.FunSpec
import io.kotest.extensions.testcontainers.TestContainerExtension
import io.kotest.matchers.collections.shouldContainOnly
import io.kotest.matchers.shouldBe
import io.ktor.client.HttpClient
import org.testcontainers.images.PullPolicy

class MainSpec : FunSpec() {
  init {
    val container = install(TestContainerExtension("ghcr.io/jamesward/easyracer")) {
      withImagePullPolicy(PullPolicy.alwaysPull())
      withExposedPorts(8080)
    }

    val client = autoClose(HttpClient())
    val scenarios = client.scenarios()

    concurrency = scenarios.size

    fun url(i: Int) = "http://localhost:${container.firstMappedPort}/$i"

    client.scenarios().forEachIndexed { index, scenario ->
      test("scenario-${index + 1}") {
        scenario(::url) shouldBe "right"
      }
    }
  }
}
