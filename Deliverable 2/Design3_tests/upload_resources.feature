Feature: Upload Training Resources

  Scenario: A trainer uploads a PDF to a module
    Given I am logged in as a trainer
    When I upload a PDF to a training module
    Then it should be available for trainees to download
