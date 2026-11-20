package edu.cnm.deepdive.petamber.server.model.entity

import jakarta.persistence.CascadeType
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.FetchType
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.Index
import jakarta.persistence.OneToMany
import jakarta.persistence.OrderBy
import jakarta.persistence.PrePersist
import jakarta.persistence.Table
import org.hibernate.annotations.CreationTimestamp
import java.util.UUID
import kotlin.time.Instant

@Entity
@Table(
    name = "user_profile",
    indexes = [
        Index(columnList = "created")
    ]
)
class UserProfile(

    @Column(name = "oauth_key", unique = true, nullable = false, updatable = false, length = 255)
    var oauthKey: String,

    @Column(unique = true, nullable = false, length = 255)
    var email: String,

    @Column(name = "display_name", nullable = false, length = 100)
    var displayName: String,

    @Column(name = "avatar_url", nullable = true, length = 1024)
    var avatarUrl: String? = null,

    @Column(name = "phone_number", nullable = true, length = 30)
    var phoneNumber: String? = null

) {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_profile_id", nullable = false, updatable = false)
    var id: Long? = null

    @Column(name = "external_key", nullable = false, updatable = false, unique = true)
    var externalKey: UUID? = null

    @Column(nullable = false, updatable = false)
    @CreationTimestamp
    open var created: Instant? = null

    @OneToMany(
        mappedBy = "owner",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("created DESC")
    private val _petReports: MutableList<PetReport> = mutableListOf()

    val petReports: List<PetReport>
        get() = _petReports.toList()

    @OneToMany(
        mappedBy = "user",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("joined DESC")
    private val _squadMemberships: MutableList<SquadMembership> = mutableListOf()

    val squadMemberships: List<SquadMembership>
        get() = _squadMemberships.toList()

    @OneToMany(
        mappedBy = "spotter",
        fetch = FetchType.LAZY
    )
    @OrderBy("sightingTimestamp DESC")
    private val _sightings: MutableList<Sighting> = mutableListOf()

    val sightings: List<Sighting>
        get() = _sightings.toList()

    @OneToMany(
        mappedBy = "user",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("created DESC")
    private val _corroborations: MutableList<Corroboration> = mutableListOf()

    val corroborations: List<Corroboration>
        get() = _corroborations.toList()

    @PrePersist
    fun generateFieldValues() {
        if (externalKey == null) {
            externalKey = UUID.randomUUID()
        }
    }

}
