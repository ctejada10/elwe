import StoreKit

let authorization = await SKCloudServiceController.requestAuthorization()
let userToken = try await SKCloudServiceController().requestUserToken(forDeveloperToken: "")

print(userToken)
